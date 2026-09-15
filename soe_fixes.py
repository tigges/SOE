#!/usr/bin/env python3
"""
SOE fix generator — turns findings.json + the config into a paste-ready fix pack.

Usage:
    python soe_fixes.py configs/<slug>.yaml reports/<slug>/<date> [--llm]

Writes <report dir>/fixes.md (and fixes.json) containing:
  1. Entity JSON-LD built from the config (business, hours, geo, profiles, booking)
  2. Per-page title / meta description / H1 proposals
       - default: rule-based drafts (clearly marked DRAFT)
       - --llm with ANTHROPIC_API_KEY: drafted by Claude (model from env SOE_MODEL)
       - in a Claude session: the /soe skill asks Claude to replace the drafts directly
  3. Platform steps for every finding (from fixpacks/<platform>.yaml)
  4. An llms.txt summary and a Q&A block drafted from keywords.questions
Every proposal is for human approval before publishing.
"""
import argparse, json, os, re

import requests, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_TYPE = {"local_business": "LocalBusiness", "saas": "SoftwareApplication", "ecommerce": "OnlineStore",
               "publisher": "NewsMediaOrganization", "personal_brand": "Person", "generic": "Organization"}


def e164_uk(phone):
    d = re.sub(r"\D", "", phone or "")
    return "+44" + d[1:] if d.startswith("0") else ("+" + d if d else "")


def entity_jsonld(cfg):
    s, b = cfg["site"], cfg.get("business") or {}
    t = s.get("schema_type") or SCHEMA_TYPE.get(s.get("type"), "Organization")
    url = s["url"].rstrip("/") + "/"
    j = {"@context": "https://schema.org", "@type": t, "@id": url + "#entity",
         "name": b.get("name") or s.get("name"), "url": url}
    if s.get("description"):
        j["description"] = s["description"]
    if b.get("phone"):
        j["telephone"] = e164_uk(b["phone"])
    if b.get("email"):
        j["email"] = b["email"]
    if b.get("price_range"):
        j["priceRange"] = b["price_range"]
    if b.get("address"):
        parts = [p.strip() for p in b["address"].split(",")]
        j["address"] = {"@type": "PostalAddress", "streetAddress": ", ".join(parts[:2]) if len(parts) > 2 else parts[0],
                        "addressLocality": parts[-2] if len(parts) > 2 else (parts[-1] if len(parts) > 1 else ""),
                        "addressRegion": parts[-1] if len(parts) > 2 else "",
                        "postalCode": b.get("postcode", ""), "addressCountry": s.get("country", "GB")}
    g = b.get("geo") or {}
    if g.get("lat") is not None and g.get("lng") is not None:
        j["geo"] = {"@type": "GeoCoordinates", "latitude": g["lat"], "longitude": g["lng"]}
    if b.get("hours"):
        j["openingHoursSpecification"] = [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"],
                                           "opens": h["opens"], "closes": h["closes"]} for h in b["hours"]]
    prof = b.get("profiles") or {}
    same = [v for k, v in prof.items() if v and k != "booking"]
    if same:
        j["sameAs"] = same
    if prof.get("booking"):
        j["potentialAction"] = {"@type": "ReserveAction", "target": prof["booking"]}
    return j


def locality(cfg):
    kws = (cfg.get("keywords") or {}).get("primary") or []
    m = re.search(r"\b(?:in\s+)?([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)$", kws[0]) if kws else None
    return m.group(1) if m else ""


def rule_drafts(cfg, pages):
    brand = (cfg.get("business") or {}).get("name") or cfg["site"].get("name")
    kws = (cfg.get("keywords") or {}).get("primary") or []
    out = []
    for p in pages:
        path = p["url"].split("//", 1)[-1].split("/", 1)[-1] if "/" in p["url"].split("//", 1)[-1] else ""
        topic = (p["h1"][0] if p["h1"] else re.split(r"\s[|\-–]\s", p["title"])[0]).strip().title()
        topic = re.sub(r"\b(\w) (?=\w\b)", r"\1", topic)          # "H O M E" -> "HOME"
        if not path and kws:
            topic = kws[0][0].upper() + kws[0][1:]
        title = f"{topic} | {brand}"
        loc = locality(cfg)
        cta = {"local_business": "See prices and opening hours, and book online.",
               "saas": "See features and pricing, and start free.",
               "ecommerce": "Browse the range with fast UK delivery.",
               "personal_brand": "Listen, see upcoming dates and get in touch for bookings.",
               "publisher": "Read the latest coverage and analysis."}.get(cfg["site"].get("type"), "Find out more and get in touch.")
        desc = f"{topic} at {brand}{' in ' + loc if loc and loc.lower() not in topic.lower() else ''}. {cta}"
        out.append(dict(url=p["url"], current_title=p["title"], title=title[:60], description=desc[:160],
                        h1=topic, source="DRAFT (rule-based)"))
    return out


def llm_drafts(cfg, pages, findings):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("--llm skipped: ANTHROPIC_API_KEY not set; using rule-based drafts")
        return None
    brief = dict(site=cfg["site"], business=cfg.get("business"), keywords=cfg.get("keywords"),
                 pages=[{k: p[k] for k in ("url", "title", "description", "h1", "words")} for p in pages],
                 findings=[{k: f[k] for k in ("check", "detail", "url")} for f in findings][:60])
    prompt = ("You are an SEO copywriter. For each page, propose: title (50-60 chars, primary topic + place/brand), "
              "description (140-160 chars, factual, with a call to action), h1. Use only facts in the brief; "
              "map each primary keyword to one page. Reply with a JSON array of objects "
              "{url,title,description,h1} and nothing else.\n\nBRIEF:\n" + json.dumps(brief, default=str))
    r = requests.post("https://api.anthropic.com/v1/messages", timeout=120,
                      headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                      json={"model": os.environ.get("SOE_MODEL", "claude-sonnet-4-5"), "max_tokens": 4000,
                            "messages": [{"role": "user", "content": prompt}]})
    r.raise_for_status()
    text = "".join(c.get("text", "") for c in r.json().get("content", []))
    rows = json.loads(text[text.index("["): text.rindex("]") + 1])
    cur = {p["url"]: p["title"] for p in pages}
    for row in rows:
        row.update(current_title=cur.get(row["url"], ""), source="Claude draft")
    return rows


def llms_summary(cfg):
    s, b = cfg["site"], cfg.get("business") or {}
    bits = [f"{b.get('name') or s.get('name')}"]
    if s.get("description"):
        bits.append(s["description"])
    if b.get("address"):
        bits.append(f"Address: {b['address']} {b.get('postcode', '')}.")
    if b.get("hours"):
        bits.append("Hours: " + "; ".join(f"{', '.join(d[:3] for d in h['days'])} {h['opens']}–{h['closes']}"
                                          for h in b["hours"]) + ".")
    if b.get("phone"):
        bits.append(f"Phone {b['phone']}.")
    if (b.get("profiles") or {}).get("booking"):
        bits.append(f"Book online: {b['profiles']['booking']}")
    return " ".join(bits)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("report_dir")
    ap.add_argument("--llm", action="store_true")
    ap.add_argument("--copy", help="YAML of reviewed/Claude-written copy: [{url, title, description, h1}] — overrides drafts")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    rep = json.load(open(os.path.join(a.report_dir, "findings.json")))
    pages, findings = rep["pages"], rep["findings"]
    drafts = (llm_drafts(cfg, pages, findings) if a.llm else None) or rule_drafts(cfg, pages)
    if a.copy and os.path.exists(a.copy):
        written = {c["url"].rstrip("/"): c for c in yaml.safe_load(open(a.copy)) or []}
        for d in drafts:
            c = written.get(d["url"].rstrip("/"))
            if c:
                d.update({k: c[k] for k in ("title", "description", "h1") if c.get(k)}, source=c.get("source", "Claude draft"))
                if c.get("new_url"):
                    d["new_url"] = c["new_url"]
    schema = entity_jsonld(cfg)
    steps = {}
    for f in findings:
        steps.setdefault(f["check"], dict(fix=f["fix"], how=f.get("how"), count=0, severity=f["severity"]))
        steps[f["check"]]["count"] += 1
    qs = (cfg.get("keywords") or {}).get("questions") or []
    pack = dict(schema=schema, pages=drafts, steps=steps, llms_summary=llms_summary(cfg), questions=qs)
    json.dump(pack, open(os.path.join(a.report_dir, "fixes.json"), "w"), indent=2)

    plat = cfg["site"].get("platform", "the platform")
    L = [f"# Fix pack — {cfg['site'].get('name')}", "",
         "Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — "
         "have Claude rewrite it (the /soe skill does this) or run with --llm.", "",
         "## 1. Entity structured data (JSON-LD)", "", "```json", json.dumps(schema, indent=2, ensure_ascii=False), "```", "",
         "## 2. Page titles, descriptions, H1", "", "| Page | Now | Proposed title | Proposed description | H1 | Source |",
         "|---|---|---|---|---|---|"]
    cell = lambda x: str(x or "").replace("|", "\\|")
    for d in drafts:
        L.append("| " + " | ".join(cell(d.get(k)) for k in ("url", "current_title", "title", "description", "h1", "source")) + " |")
    L += ["", f"## 3. Steps on {plat}", ""]
    for k, v in sorted(steps.items(), key=lambda kv: -{"critical": 4, "high": 3, "medium": 2, "low": 1}[kv[1]["severity"]]):
        L.append(f"- **{k}** ({v['severity']}, ×{v['count']}) — {v['fix']}" + (f"  \n  _How:_ {v['how']}" if v.get("how") else ""))
    L += ["", "## 4. llms.txt summary", "", "> " + pack["llms_summary"], ""]
    if qs:
        L += ["## 5. Q&A block (visible on the page; answers to be written from real facts)", ""]
        L += [f"**{q}**  \n_Answer: …_" for q in qs]
    open(os.path.join(a.report_dir, "fixes.md"), "w").write("\n".join(L) + "\n")
    print(f"fix pack → {a.report_dir}/fixes.md ({len(drafts)} pages, {len(steps)} fix types)")


if __name__ == "__main__":
    main()

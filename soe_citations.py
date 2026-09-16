#!/usr/bin/env python3
"""
SOE citations checker — are off-site listings consistent with the canonical business name, address and phone?

Usage:
    python soe_citations.py configs/<slug>.yaml [--out reports/<slug>/<date>]

For each `citations:` entry in the config it fetches the listing and checks for:
  name   – the canonical business name (or one of ai.brand_terms), case-insensitive
  phone  – last 9 digits of business.phone, ignoring formatting (+44 / 0 prefixes)
  postcode – business.postcode, ignoring spaces
Entries marked `manual: true` (social networks that block bots) are listed for a human check.
Entries marked `ignore: true` / `unrelated: true` are skipped (wrong business, scraped aggregator, etc.).
Entries marked `action: list` (or with no URL) are remembered as "to list" — create/claim the
directory and set the website to the canonical site URL.
It also compares the listings against the vertical module's directory list and reports
directories with no known listing ("gaps"). Tracked to-list rows fill that directory's gap.

Writes citations.json and citations.md into the output folder.
"""
import argparse, datetime as dt, json, os, re

import requests, yaml
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (compatible; SOE-Audit/1.0)"


def digits(s):
    return re.sub(r"\D", "", s or "")


def check(entry, b, names):
    row = dict(source=entry.get("source"), url=entry.get("url") or "", directory=entry.get("directory"),
               note=entry.get("note", ""), action=entry.get("action") or "")
    if entry.get("ignore") or entry.get("unrelated"):
        row.update(status="ignore", detail="Not a listing for this business — skip")
        return row
    if entry.get("action") == "list" or not (entry.get("url") or "").strip():
        row.update(status="todo", detail="Not listed yet — add the canonical site URL")
        return row
    if entry.get("manual"):
        row.update(status="manual", detail="Blocks automated reading — check by hand")
        return row
    try:
        r = requests.get(entry["url"], headers={"User-Agent": UA}, timeout=25)
    except requests.RequestException as e:
        row.update(status="unreachable", detail=str(e)[:120])
        return row
    if r.status_code >= 400:
        row.update(status="unreachable", detail=f"HTTP {r.status_code}")
        return row
    text = BeautifulSoup(r.text, "lxml").get_text(" ", strip=True)
    low, flat = text.lower(), digits(text)
    got = {
        "name": any(n.lower() in low for n in names),
        "phone": bool(b.get("phone")) and digits(b["phone"])[-9:] in flat,
        "postcode": bool(b.get("postcode")) and b["postcode"].replace(" ", "").lower() in low.replace(" ", ""),
    }
    # any other UK postcode / phone on the page hints at a stale address
    other_pc = sorted({p.upper() for p in re.findall(r"\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b", text, re.I)
                       if p.replace(" ", "").lower() != (b.get("postcode") or "").replace(" ", "").lower()})[:3]
    missing = [k for k, v in got.items() if not v]
    status = "ok" if not missing else "mismatch"
    detail = "name, phone and postcode match" if not missing else f"not found: {', '.join(missing)}"
    if other_pc and missing:
        detail += f" · other postcode(s) on page: {', '.join(other_pc)}"
    row.update(status=status, detail=detail, checks=got)
    return row


ACTIONS = {"take_offline": "Take it offline (delete the site or the listing on that platform)",
           "redirect": "301-redirect the whole domain to the main site"}


def source_md(row):
    url = (row.get("url") or "").strip()
    name = row.get("source") or url or "listing"
    return f"[{name}]({url})" if url.startswith("http") else name


def directory_gaps(dirs, rows):
    """Directories from the vertical module that have no tracked listing.

    Ignore/unrelated rows do not count. To-list rows do: they are remembered
    actions, so they leave the anonymous gap list and show as status=todo.
    """
    have = " ".join(f"{r.get('source') or ''} {r.get('url') or ''}".lower()
                    for r in rows if r.get("status") != "ignore")
    gaps = {grp: [d for d in lst if d.split()[0].lower() not in have] for grp, lst in (dirs or {}).items()}
    return {k: v for k, v in gaps.items() if v}


def check_legacy(entry, main_url):
    """Is an old/parked site still live? Anything reachable that isn't a redirect to the main site is a problem."""
    row = dict(url=entry["url"], action=entry.get("action", "take_offline"), note=entry.get("note", ""))
    row["recommendation"] = ACTIONS.get(row["action"], row["action"])
    try:
        r = requests.get(entry["url"], headers={"User-Agent": UA}, timeout=25, allow_redirects=True)
    except requests.RequestException as e:
        row.update(status="offline", detail=f"not reachable ({type(e).__name__}) — done")
        return row
    main_host = main_url.split("//")[-1].split("/")[0].replace("www.", "")
    final_host = r.url.split("//")[-1].split("/")[0].replace("www.", "")
    if final_host == main_host:
        row.update(status="redirected", detail=f"redirects to {r.url} — done")
    elif r.status_code >= 400:
        row.update(status="offline", detail=f"HTTP {r.status_code} — done")
    else:
        title = BeautifulSoup(r.text, "lxml").title
        row.update(status="live", detail=f"still live (HTTP {r.status_code}): '{(title.string or '').strip()[:80] if title else ''}'")
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    b = cfg.get("business") or {}
    domain = cfg["site"]["url"].split("//")[-1].replace("www.", "").strip("/")
    names = [b.get("name", "")] + (cfg.get("ai", {}).get("brand_terms") or []) + [domain]
    names = [n for n in names if n]
    rows = [check(e, b, names) for e in cfg.get("citations") or []]
    legacy = [check_legacy(e, cfg["site"]["url"]) for e in cfg.get("legacy_sites") or [] if e.get("url")]
    clashes = cfg.get("name_clashes") or []

    ptype = cfg["site"].get("type", "generic")
    mpath = os.path.join(HERE, "modules", f"{ptype}.yaml")
    dirs = (yaml.safe_load(open(mpath)) or {}).get("directories", {}) if os.path.exists(mpath) else {}
    gaps = directory_gaps(dirs, rows)

    out = a.out or os.path.join(HERE, "reports", cfg["site"].get("slug", "site"), dt.date.today().isoformat())
    os.makedirs(out, exist_ok=True)
    summary = {s: sum(r["status"] == s for r in rows)
               for s in ("ok", "mismatch", "unreachable", "manual", "todo", "ignore")}
    json.dump(dict(run=dt.datetime.now().isoformat(timespec="minutes"), summary=summary, listings=rows, gaps=gaps,
                   legacy=legacy, name_clashes=clashes),
              open(os.path.join(out, "citations.json"), "w"), indent=2)
    L = [f"# Citations — {cfg['site'].get('name')}", "", " · ".join(f"{k}: {v}" for k, v in summary.items()), "",
         "| Status | Source | Detail | Note |", "|---|---|---|---|"]
    L += [f"| {r['status']} | {source_md(r)} | {r.get('detail','')} | {r.get('note','')} |" for r in rows]
    if legacy:
        L += ["", "## Old sites to retire", "", "| Status | Site | What we found | Do this |", "|---|---|---|---|"]
        L += [f"| {r['status']} | {r['url']} | {(r['detail'] + ' · ' + r['note']).replace('|', '/')} | {r['recommendation']} |" for r in legacy]
    if clashes:
        L += ["", "## Same-name businesses", ""] + [f"- [{c.get('name')}]({c.get('url')}) — {c.get('note', '')}" for c in clashes]
    L += ["", "## Directories with no known listing", ""] + [f"- **{g}:** {', '.join(v)}" for g, v in gaps.items()]
    open(os.path.join(out, "citations.md"), "w").write("\n".join(L) + "\n")
    print(f"citations: {summary} · legacy live: {sum(r['status'] == 'live' for r in legacy)} · gaps: {sum(len(v) for v in gaps.values())} → {out}/citations.md")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
SOE AI-visibility log — is the brand mentioned or cited when people ask AI engines?

The log is a CSV per project: data/<slug>/ai_log.csv
  date, engine, prompt, mentioned (y/n), cited (y/n), position, cited_sources, notes, method

Commands:
  python soe_ai_log.py init    configs/<slug>.yaml   # add this month's blank rows (prompts × engines) to fill by hand
  python soe_ai_log.py run     configs/<slug>.yaml   # auto-fill engines that have an API key (see below)
  python soe_ai_log.py summary configs/<slug>.yaml [--out reports/<slug>/<date>]   # → ai_visibility.json

Automated engines (optional, key-gated; answers differ from the consumer apps, so keep manual checks too):
  Perplexity  PERPLEXITY_API_KEY  POST https://api.perplexity.ai/chat/completions  (model "sonar"; returns citations)
  ChatGPT     OPENAI_API_KEY      POST https://api.openai.com/v1/responses with the web_search tool
              (model from env SOE_OPENAI_MODEL, default "gpt-4.1-mini")
Manual engines (no public API matching the product): Gemini app, Google AI Mode / AI Overviews.
"""
import argparse, collections, csv, datetime as dt, json, os, re, sys

import requests, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = ["date", "engine", "prompt", "mentioned", "cited", "position", "cited_sources", "notes", "method"]


def log_path(cfg):
    d = os.path.join(HERE, "data", cfg["site"].get("slug", "site"))
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "ai_log.csv")


def read(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in COLS})


def brand_terms(cfg):
    b = cfg.get("business") or {}
    domain = cfg["site"]["url"].split("//")[-1].replace("www.", "").strip("/")
    return [t.lower() for t in [b.get("name"), domain] + (cfg.get("ai", {}).get("brand_terms") or []) if t]


def domain_of(u):
    return re.sub(r"^www\.", "", (u or "").split("//")[-1].split("/")[0]).lower()


def init(cfg):
    path, month = log_path(cfg), dt.date.today().strftime("%Y-%m")
    rows = read(path)
    have = {(r["date"][:7], r["engine"], r["prompt"]) for r in rows}
    added = 0
    for p in cfg.get("ai", {}).get("prompts", []):
        for e in cfg.get("ai", {}).get("engines", ["ChatGPT", "Perplexity", "Gemini", "Google AI Mode"]):
            if (month, e, p) not in have:
                rows.append(dict(date=dt.date.today().isoformat(), engine=e, prompt=p, method="manual"))
                added += 1
    write(path, rows)
    print(f"{added} blank rows added → {path}  (fill mentioned/cited y/n, cited_sources as ; list)")


def score_answer(text, sources, terms, own_domain):
    low = text.lower()
    mentioned = any(t in low for t in terms)
    doms = [domain_of(s) for s in sources]
    cited = own_domain in doms
    pos = doms.index(own_domain) + 1 if cited else ""
    return dict(mentioned="y" if mentioned else "n", cited="y" if cited else "n", position=pos,
                cited_sources="; ".join(dict.fromkeys(d for d in doms if d)))


def ask_perplexity(prompt, key):
    r = requests.post("https://api.perplexity.ai/chat/completions", timeout=90,
                      headers={"Authorization": f"Bearer {key}"},
                      json={"model": "sonar", "messages": [{"role": "user", "content": prompt}]})
    r.raise_for_status()
    d = r.json()
    text = d["choices"][0]["message"]["content"]
    sources = d.get("citations") or [s.get("url") for s in d.get("search_results", [])]
    return text, sources


def ask_openai(prompt, key):
    r = requests.post("https://api.openai.com/v1/responses", timeout=120,
                      headers={"Authorization": f"Bearer {key}"},
                      json={"model": os.environ.get("SOE_OPENAI_MODEL", "gpt-4.1-mini"),
                            "tools": [{"type": "web_search"}], "input": prompt})
    r.raise_for_status()
    text, sources = "", []
    for item in r.json().get("output", []):
        for c in item.get("content", []) or []:
            if c.get("type") == "output_text":
                text += c.get("text", "")
                sources += [a.get("url") for a in c.get("annotations", []) if a.get("type") == "url_citation"]
    return text, sources


def run(cfg):
    engines = {"Perplexity": ("PERPLEXITY_API_KEY", ask_perplexity), "ChatGPT": ("OPENAI_API_KEY", ask_openai)}
    path, today = log_path(cfg), dt.date.today().isoformat()
    rows, terms = read(path), brand_terms(cfg)
    own = domain_of(cfg["site"]["url"])
    for name, (env, fn) in engines.items():
        key = os.environ.get(env)
        if not key:
            print(f"skipped {name}: {env} not set")
            continue
        for p in cfg.get("ai", {}).get("prompts", []):
            try:
                text, sources = fn(p, key)
                res = score_answer(text, sources, terms, own)
                rows.append(dict(date=today, engine=name, prompt=p, method="api",
                                 notes=text[:200].replace("\n", " "), **res))
                print(f"  {name} · {p[:40]} · mentioned {res['mentioned']} · cited {res['cited']}")
            except Exception as e:
                print(f"  {name} error: {str(e)[:120]}", file=sys.stderr)
    write(path, rows)


def summary(cfg, out):
    rows = [r for r in read(log_path(cfg)) if r.get("mentioned") in ("y", "n")]
    by_month = collections.defaultdict(list)
    for r in rows:
        by_month[r["date"][:7]].append(r)
    months = []
    for m in sorted(by_month):
        rs = by_month[m]
        eng = collections.defaultdict(lambda: [0, 0, 0])
        for r in rs:
            e = eng[r["engine"]]
            e[0] += 1; e[1] += r["mentioned"] == "y"; e[2] += r.get("cited") == "y"
        months.append(dict(month=m, checks=len(rs),
                           mention_rate=round(sum(r["mentioned"] == "y" for r in rs) / len(rs), 2),
                           citation_rate=round(sum(r.get("cited") == "y" for r in rs) / len(rs), 2),
                           engines={k: dict(checks=v[0], mentioned=v[1], cited=v[2]) for k, v in eng.items()}))
    own = domain_of(cfg["site"]["url"])
    src = collections.Counter(s.strip() for r in rows for s in (r.get("cited_sources") or "").split(";")
                              if s.strip() and s.strip() != own)
    pending = sum(1 for r in read(log_path(cfg)) if not r.get("mentioned"))
    res = dict(months=months, top_other_sources=src.most_common(15), pending_checks=pending,
               prompts=cfg.get("ai", {}).get("prompts", []), engines=cfg.get("ai", {}).get("engines", []))
    if out:
        os.makedirs(out, exist_ok=True)
        json.dump(res, open(os.path.join(out, "ai_visibility.json"), "w"), indent=2)
    print(json.dumps(res, indent=2)[:800])
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["init", "run", "summary"])
    ap.add_argument("config")
    ap.add_argument("--out")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    {"init": lambda: init(cfg), "run": lambda: run(cfg), "summary": lambda: summary(cfg, a.out)}[a.cmd]()


if __name__ == "__main__":
    main()

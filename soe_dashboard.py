#!/usr/bin/env python3
"""
SOE dashboard generator — builds the SOE Control Room page from every report on disk.

Usage:
    python soe_dashboard.py [--out dashboard/dist/soe-control-room.html]
    python soe_dashboard.py --standalone --out index.html     # GitHub Pages (https://tigges.github.io/SOE/)

Reads configs/*.yaml (including sites that have not been audited yet), reports/<slug>/<date>/*.json and data/<slug>/ai_log.csv, embeds them
as JSON into dashboard/template.html, and writes one self-contained page (no <html>/<head>,
ready for the Artifact publisher; use --standalone for a full HTML document).
"""
import argparse, csv, glob, json, os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))


def jload(path):
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return None


def project(cfg_path):
    cfg = yaml.safe_load(open(cfg_path))
    slug = cfg["site"].get("slug")
    b = cfg.get("business") or {}
    base = dict(
        slug=slug, name=cfg["site"].get("name"), pinned=bool(cfg["site"].get("pinned")),
        url=cfg["site"]["url"], type=cfg["site"].get("type"), platform=cfg["site"].get("platform"),
        module=None, keywords=cfg.get("keywords") or {},
        prompts=(cfg.get("ai") or {}).get("prompts") or [],
        engines=(cfg.get("ai") or {}).get("engines") or [],
        business=dict(name=b.get("name"), phone=b.get("phone"), postcode=b.get("postcode")),
        runs=[], latest=None, audit=None, competitors=None, citations=None, fixes=None,
        integrations={"results": {}}, benchmark=None, ai_summary=None, ai_rows=[], pending=True,
    )
    run_dirs = sorted(d for d in glob.glob(os.path.join(HERE, "reports", slug, "*")) if os.path.isdir(d))
    runs = []
    for d in run_dirs:
        f = jload(os.path.join(d, "findings.json"))
        if f:
            runs.append(dict(date=os.path.basename(d), score=f["score"], layers=f["layers"],
                             findings=len(f["findings"])))
    if not runs:
        return base
    latest = run_dirs[-1]
    f = jload(os.path.join(latest, "findings.json"))
    for p in f["pages"]:
        for k in ("raw_html", "text"):
            p.pop(k, None)
    integ = jload(os.path.join(latest, "integrations.json")) or {"results": {}}
    res = integ.setdefault("results", {})
    if not res.get("gsc"):
        # a Search Console export stays valid across later runs: use the newest gsc.json for this site
        exports = sorted(glob.glob(os.path.join(HERE, "reports", slug, "*", "gsc.json")))
        if exports:
            res["gsc"] = jload(exports[-1])
    idx = jload(os.path.join(latest, "indexnow.json"))
    if idx and not res.get("indexnow"):
        res["indexnow"] = idx.get("summary") or idx
    ai_rows = []
    ap = os.path.join(HERE, "data", slug, "ai_log.csv")
    if os.path.exists(ap):
        ai_rows = list(csv.DictReader(open(ap, newline="")))
    base.update(dict(
        pending=False, module=(f.get("project") or {}).get("module"),
        runs=runs, latest=os.path.basename(latest), audit=f,
        competitors=jload(os.path.join(latest, "competitors.json")),
        citations=jload(os.path.join(latest, "citations.json")),
        fixes=jload(os.path.join(latest, "fixes.json")),
        integrations=integ,
        benchmark=(lambda b: b and {k: v for k, v in b.items() if k != "inventory"})(jload(os.path.join(latest, "benchmark.json"))),
        ai_summary=jload(os.path.join(latest, "ai_visibility.json")), ai_rows=ai_rows,
    ))
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "dashboard", "dist", "soe-control-room.html"))
    ap.add_argument("--standalone", action="store_true")
    a = ap.parse_args()
    projects = [p for c in sorted(glob.glob(os.path.join(HERE, "configs", "*.yaml")))
                if not os.path.basename(c).startswith("_") for p in [project(c)] if p]
    modules = {os.path.basename(m)[:-5]: (yaml.safe_load(open(m)) or {}).get("label")
               for m in sorted(glob.glob(os.path.join(HERE, "modules", "*.yaml")))}
    packs = {os.path.basename(m)[:-5]: len((yaml.safe_load(open(m)) or {}).get("fixes", {}))
             for m in sorted(glob.glob(os.path.join(HERE, "fixpacks", "*.yaml")))}
    projects.sort(key=lambda p: (not p.get("pinned"), p["name"].lower()))
    repo = os.environ.get("GITHUB_REPOSITORY") or "tigges/SOE"
    data = dict(projects=projects, modules=modules, fixpacks=packs, repo=repo,
                platforms=["wix", "wordpress", "webflow", "shopify", "nextjs", "other"])
    tpl = open(os.path.join(HERE, "dashboard", "template.html")).read()
    html = tpl.replace("__DATA__", json.dumps(data, default=str).replace("</", "<\\/"))
    if a.standalone:
        # full document for GitHub Pages: title, fonts and styles go in <head>; noindex keeps client data out of search
        cut = html.index("</style>") + len("</style>")
        html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
                '<meta name="robots" content="noindex,nofollow">\n' + html[:cut] + "\n</head><body>\n"
                + html[cut:] + "\n</body></html>\n")
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w").write(html)
    print(f"dashboard → {a.out} ({len(projects)} projects, {os.path.getsize(a.out)//1024} KB)")


if __name__ == "__main__":
    main()

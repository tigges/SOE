#!/usr/bin/env python3
"""
SOE Search Console import — use a manual Search Console export instead of the API (no Google Cloud needed).

How to export: search.google.com/search-console → Performance → Search results → set the date range
(e.g. Last 3 months) → Export → Download CSV. You get a .zip with Chart, Queries, Pages, Countries,
Devices, Search appearance and Filters CSVs.

Usage:
    python soe_gsc_import.py configs/<slug>.yaml <export.zip or folder> [--out reports/<slug>/<date>]

What it does
  - keeps the raw CSVs in data/<slug>/gsc/<export date>/ (so history builds up over time)
  - writes <report dir>/gsc.json (same summary shape as integrations/gsc.py, plus daily chart,
    pages, countries, devices and plain-English insights)
  - records the result as the "gsc" source in <report dir>/integrations.json, so the dashboard's
    Search Console card shows it (marked "CSV export")
The report dir defaults to the newest reports/<slug>/<date> folder.
"""
import argparse, csv, datetime as dt, glob, io, json, os, re, zipfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {"chart": "Chart.csv", "queries": "Queries.csv", "pages": "Pages.csv", "countries": "Countries.csv",
         "devices": "Devices.csv", "appearance": "Search appearance.csv", "filters": "Filters.csv"}


def num(v, pct=False):
    v = (v or "").strip().replace(",", "")
    if not v:
        return None
    if v.endswith("%"):
        return round(float(v[:-1]) / 100, 4)
    return float(v) if "." in v else int(v)


def read_export(path):
    """Return {kind: [row dicts]} from a zip or a folder of CSVs."""
    blobs = {}
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            for n in z.namelist():
                blobs[os.path.basename(n)] = z.read(n).decode("utf-8-sig")
    else:
        for f in glob.glob(os.path.join(path, "*.csv")):
            blobs[os.path.basename(f)] = open(f, encoding="utf-8-sig").read()
    out = {}
    for kind, fname in FILES.items():
        text = blobs.get(fname)
        if text is None:
            continue
        rows = list(csv.reader(io.StringIO(text)))
        if not rows:
            out[kind] = []
            continue
        head = rows[0]
        out[kind] = [dict(zip(head, r)) for r in rows[1:] if any(c.strip() for c in r)]
    out["_raw"] = blobs
    return out


def metrics(r):
    return dict(clicks=num(r.get("Clicks")) or 0, impressions=num(r.get("Impressions")) or 0,
                ctr=num(r.get("CTR")), position=num(r.get("Position")))


def rollup(rows):
    clicks = sum(r["clicks"] for r in rows)
    impr = sum(r["impressions"] for r in rows)
    pw = sum((r["position"] or 0) * r["impressions"] for r in rows if r["position"] is not None)
    return dict(clicks=clicks, impressions=impr, ctr=round(clicks / impr, 4) if impr else None,
                position=round(pw / impr, 1) if impr else None)


def insights(s, cfg):
    tips = []
    t = s["totals"]
    days = len(s["daily"]) or 1
    tips.append(f"{t['impressions']} impressions and {t['clicks']} click{'s' if t['clicks'] != 1 else ''} in {days} days "
                f"(about {round(t['impressions'] / days * 30)} impressions a month).")
    if t["position"] and t["position"] > 10:
        tips.append(f"Average position {t['position']}: the site mostly appears on page 2, where few people click. "
                    "Moving onto page 1 is the main lever.")
    brand = [b.lower() for b in [(cfg.get("business") or {}).get("name", ""), cfg["site"].get("name", "")] +
             ((cfg.get("ai") or {}).get("brand_terms") or []) if b]
    bq = [q for q in s["top_queries"] if any(re.sub(r"\W", "", b) in re.sub(r"\W", "", q["query"]) for b in brand)]
    if bq and len(bq) == len(s["top_queries"]):
        tips.append("Every query is a brand search: people already looking for the name. "
                    "No non-brand keyword brings impressions yet, so pages need to target what fans search for.")
    for q in s["top_queries"]:
        if q["position"] and q["position"] > 3 and any(re.sub(r"\W", "", b) == re.sub(r"\W", "", q["query"]) for b in brand):
            tips.append(f"Searching the exact name \"{q['query']}\" puts the site at position {q['position']}; "
                        "a brand should rank #1. Clear name + entity markup (Person/MusicGroup, sameAs) fixes this.")
            break
    near = [q["query"] for q in s["top_queries"] if q["query"] not in [x["query"] for x in bq]]
    if near:
        tips.append(f"Near-miss spellings also show the site: {', '.join(near[:4])}. Mention the name clearly so Google connects them.")
    if s["pages"] and s["pages"][0]["impressions"] >= 0.9 * max(t["impressions"], 1):
        tips.append("Almost all impressions land on the homepage; other pages are invisible in search.")
    dev = {d["device"]: d for d in s["devices"]}
    if dev.get("Desktop") and dev.get("Mobile") and dev["Mobile"]["position"] and dev["Desktop"]["position"]:
        if dev["Mobile"]["position"] + 3 < dev["Desktop"]["position"]:
            tips.append(f"Mobile ranks far better (position {dev['Mobile']['position']}) than desktop ({dev['Desktop']['position']}).")
    if s["countries"]:
        top = [c["country"] for c in s["countries"][:3]]
        tips.append(f"Most impressions come from {', '.join(top)}.")
    return tips


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("export")
    ap.add_argument("--out")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    slug = cfg["site"]["slug"]
    ex = read_export(a.export)
    if "chart" not in ex:
        raise SystemExit("Chart.csv not found — is this a Search Console Performance export?")

    daily = [dict(date=r["Date"], **metrics(r)) for r in ex["chart"]]
    daily.sort(key=lambda r: r["date"])
    filt = {r.get("Filter"): r.get("Value") for r in ex.get("filters", [])}
    top_q = [dict(query=r.get("Top queries"), **metrics(r)) for r in ex.get("queries", [])]
    pages = [dict(page=r.get("Top pages"), **metrics(r)) for r in ex.get("pages", [])]
    countries = sorted((dict(country=r.get("Country"), **metrics(r)) for r in ex.get("countries", [])),
                       key=lambda c: (-c["impressions"], -c["clicks"]))
    devices = [dict(device=r.get("Device"), **metrics(r)) for r in ex.get("devices", [])]
    kws = {}
    for k in ((cfg.get("keywords") or {}).get("primary") or []) + ((cfg.get("keywords") or {}).get("secondary") or []):
        m = [q for q in top_q if k.lower() in (q["query"] or "").lower()]
        kws[k] = rollup(m) if m else None

    m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(a.export))
    exported = m.group(1) if m else dt.date.today().isoformat()
    summary = dict(source="export", exported=exported, period=filt.get("Date"), search_type=filt.get("Search type"),
                   start=daily[0]["date"] if daily else None, end=daily[-1]["date"] if daily else None,
                   totals=rollup(daily), daily=daily, top_queries=top_q[:20], pages=pages[:20],
                   countries=countries[:10], devices=devices, keywords=kws,
                   note="from a manual Search Console export; queries list is Google's top list, not every query")
    summary["insights"] = insights(summary, cfg)

    # keep the raw export for history
    keep = os.path.join(HERE, "data", slug, "gsc", exported)
    os.makedirs(keep, exist_ok=True)
    for name, text in ex["_raw"].items():
        open(os.path.join(keep, name), "w", encoding="utf-8").write(text)

    out = a.out or sorted(d for d in glob.glob(os.path.join(HERE, "reports", slug, "*")) if os.path.isdir(d))[-1]
    json.dump(summary, open(os.path.join(out, "gsc.json"), "w"), indent=2)
    ip = os.path.join(out, "integrations.json")
    integ = json.load(open(ip)) if os.path.exists(ip) else {"site": cfg["site"]["url"], "results": {}}
    integ.setdefault("results", {})["gsc"] = summary
    json.dump(integ, open(ip, "w"), indent=2)
    t = summary["totals"]
    print(f"Search Console export {exported} ({summary['period']}): {t['impressions']} impressions, {t['clicks']} clicks, "
          f"CTR {t['ctr']}, avg position {t['position']} → {out}/gsc.json")
    for tip in summary["insights"]:
        print(" -", tip)


if __name__ == "__main__":
    main()

"""Google Search Console — Search Analytics (last 28 days, ending today-3 to allow for data lag).

Env: GSC_SERVICE_ACCOUNT_JSON = path to a service-account key file.
Setup: Cloud console > enable "Google Search Console API" > create service account + JSON key;
then in Search Console > Settings > Users and permissions, add the service-account e-mail (Restricted is enough).
Property: cfg.site.gsc_property, default "sc-domain:<host without www>" (use "https://www.x.com/" for URL-prefix props).
Needs: pip install google-auth
Docs: https://developers.google.com/webmaster-tools/v1/searchanalytics/query
"""
import datetime as dt
import os
from urllib.parse import quote

import requests

from ._common import all_keywords, cli, env, google_session, host, http_error, skip, today, write_json

NAME = "gsc"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
ENDPOINT = "https://www.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"


def agg(rows):
    clicks = sum(r["clicks"] for r in rows)
    impr = sum(r["impressions"] for r in rows)
    pos = sum(r["position"] * r["impressions"] for r in rows) / impr if impr else None
    return {"clicks": clicks, "impressions": impr, "ctr": round(clicks / impr, 4) if impr else None,
            "position": round(pos, 1) if pos is not None else None, "rows": len(rows)}


def run(cfg: dict, outdir: str) -> dict | None:
    sa = env("GSC_SERVICE_ACCOUNT_JSON")
    if not sa:
        return skip(NAME, "GSC_SERVICE_ACCOUNT_JSON not set")
    if not os.path.isfile(sa):
        return {"error": f"GSC_SERVICE_ACCOUNT_JSON file not found: {sa}"}
    prop = cfg["site"].get("gsc_property") or f"sc-domain:{host(cfg, strip_www=True)}"
    end = today() - dt.timedelta(days=3)
    start = end - dt.timedelta(days=27)
    try:
        s = google_session(sa, SCOPES, NAME)
    except Exception as e:  # missing lib / bad key file
        return {"error": str(e)}
    url = ENDPOINT.format(site=quote(prop, safe=""))
    try:
        r = s.post(url, json={"startDate": start.isoformat(), "endDate": end.isoformat(),
                              "dimensions": ["query", "page"], "rowLimit": 250}, timeout=60)
    except requests.RequestException as e:
        return http_error(e)
    if not r.ok:
        return http_error(r)
    raw = r.json()
    rows = [dict(query=x["keys"][0], page=x["keys"][1], clicks=x.get("clicks", 0),
                 impressions=x.get("impressions", 0), ctr=x.get("ctr", 0), position=x.get("position", 0))
            for x in raw.get("rows", [])]
    # rows are query+page pairs; roll up per query for the top list
    by_q = {}
    for x in rows:
        by_q.setdefault(x["query"], []).append(x)
    top = sorted(({"query": q, **agg(v)} for q, v in by_q.items()),
                 key=lambda d: (-d["clicks"], -d["impressions"]))[:20]
    for d in top:
        d.pop("rows")
    kws = {k: agg([x for x in rows if k.lower() in x["query"].lower()]) for k in all_keywords(cfg)}
    summary = {"property": prop, "start": start.isoformat(), "end": end.isoformat(),
               "note": "totals are over the top 250 query/page rows, not the whole property",
               "totals": agg(rows), "top_queries": top, "keywords": kws}
    write_json(outdir, NAME, {"request": {"property": prop}, "raw": raw, "summary": summary})
    return summary


if __name__ == "__main__":
    cli(run, NAME)

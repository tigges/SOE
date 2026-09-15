"""DataForSEO v3 — organic rank + AI Overview presence/citation, local (Maps) rank, search volume.

Env: DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD (API credentials from https://app.dataforseo.com/api-access,
not your dashboard password). Pay-as-you-go; this module sends one live task per keyword, capped at 20
keywords (primary+secondary), Maps for primary keywords only, and one search-volume request.
Location: cfg.site.location (default "London,England,United Kingdom"), language "en".
Docs: https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/
      https://docs.dataforseo.com/v3/serp/google/maps/live/advanced/
      https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/live/
"""
import re

import requests

from ._common import all_keywords, cli, env, host, http_error, skip, write_json

NAME = "dataforseo"
API = "https://api.dataforseo.com/v3/"
CAP = 20


def _bare(d):
    d = (d or "").lower().strip()
    return d[4:] if d.startswith("www.") else d


def _digits(s):
    d = re.sub(r"\D", "", s or "")
    return d[-9:] if len(d) >= 9 else d  # national significant number tail; ignores +44 / 0 prefix


def _post(s, path, task):
    """POST one task; return (result_list, error_dict)."""
    try:
        r = s.post(API + path, json=[task], timeout=120)
    except requests.RequestException as e:
        return None, http_error(e)
    if not r.ok:
        return None, http_error(r)
    body = r.json()
    if body.get("status_code") != 20000:
        return None, {"error": f"{body.get('status_code')}: {body.get('status_message')}"}
    t = (body.get("tasks") or [{}])[0]
    if t.get("status_code") != 20000:
        return None, {"error": f"{t.get('status_code')}: {t.get('status_message')}"}
    return t.get("result") or [], None


def _refs(node):
    """All reference domains anywhere inside an ai_overview item (references can be nested)."""
    out = set()
    if isinstance(node, dict):
        if "references" in node and isinstance(node["references"], list):
            for ref in node["references"]:
                if isinstance(ref, dict):
                    out.add(_bare(ref.get("domain") or re.sub(r"^https?://([^/]+).*", r"\1", ref.get("url") or "")))
        for v in node.values():
            out |= _refs(v)
    elif isinstance(node, list):
        for v in node:
            out |= _refs(v)
    return out


def organic(s, kw, loc, me):
    res, err = _post(s, "serp/google/organic/live/advanced",
                     {"keyword": kw, "location_name": loc, "language_code": "en", "device": "mobile", "depth": 20})
    if err:
        return err, None
    items = (res[0].get("items") if res else None) or []
    org = [i for i in items if i.get("type") == "organic"]
    rank = next((i.get("rank_group") for i in org if _bare(i.get("domain")) == me), None)
    top, seen = [], set()
    for i in org:
        d = _bare(i.get("domain"))
        if d not in seen:
            seen.add(d)
            top.append(d)
    aio = [i for i in items if i.get("type") == "ai_overview"]
    cited = any(me in _refs(i) for i in aio) if aio else False
    return {"organic_rank": rank, "top10": top[:10], "ai_overview": bool(aio), "cited_in_ai_overview": cited}, res


def maps(s, kw, loc, biz):
    res, err = _post(s, "serp/google/maps/live/advanced",
                     {"keyword": kw, "location_name": loc, "language_code": "en", "depth": 20})
    if err:
        return err, None
    items = [i for i in ((res[0].get("items") if res else None) or []) if i.get("type") == "maps_search"]
    name = (biz.get("name") or "").lower().strip()
    phone = _digits(biz.get("phone"))
    rank = None
    for i in items:
        if (name and name in (i.get("title") or "").lower()) or (phone and _digits(i.get("phone")) == phone):
            rank = i.get("rank_group") or i.get("rank_absolute")
            break
    return {"maps_rank": rank, "maps_top3": [i.get("title") for i in items[:3]]}, res


def run(cfg: dict, outdir: str) -> dict | None:
    login, pw = env("DATAFORSEO_LOGIN"), env("DATAFORSEO_PASSWORD")
    if not (login and pw):
        return skip(NAME, "DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD not set")
    s = requests.Session()
    s.auth = (login, pw)
    loc = cfg["site"].get("location") or "London,England,United Kingdom"
    me = host(cfg, strip_www=True)
    biz = cfg.get("business") or {}
    kws = all_keywords(cfg, CAP)
    primary = {k.lower() for k in (cfg.get("keywords") or {}).get("primary") or []}
    raw, table, errors = {"organic": {}, "maps": {}, "volume": None}, {}, []

    for kw in kws:
        row = {"organic_rank": None, "maps_rank": None, "volume": None,
               "ai_overview": None, "cited_in_ai_overview": None}
        o, raw["organic"][kw] = organic(s, kw, loc, me)
        if "error" in o:
            errors.append({kw: o["error"]})
            if o["error"].startswith(("HTTP 401", "HTTP 402", "401", "402", "40100", "40200")):
                summary = {"error": f"DataForSEO auth/balance problem, aborted: {o['error']}"}
                write_json(outdir, NAME, {"raw": raw, "summary": summary})
                return summary
        else:
            row.update(o)
        if kw.lower() in primary and biz.get("name"):
            m, raw["maps"][kw] = maps(s, kw, loc, biz)
            if "error" in m:
                errors.append({f"maps:{kw}": m["error"]})
            else:
                row.update(m)
        table[kw] = row

    res, err = _post(s, "keywords_data/google_ads/search_volume/live",
                     {"keywords": kws, "location_name": loc, "language_code": "en"})
    if err:
        errors.append({"search_volume": err["error"]})
    else:
        raw["volume"] = res
        for item in res or []:
            for kw in table:
                if kw.lower() == (item.get("keyword") or "").lower():
                    table[kw]["volume"] = item.get("search_volume")

    summary = {"location": loc, "domain": me, "keywords": table}
    if errors:
        summary["errors"] = errors
    if errors and all(r["organic_rank"] is None and r["volume"] is None for r in table.values()) \
            and len(errors) >= len(kws):
        summary["error"] = "all DataForSEO calls failed (check credentials/balance)"
    write_json(outdir, NAME, {"raw": raw, "summary": summary})
    return summary


if __name__ == "__main__":
    cli(run, NAME)

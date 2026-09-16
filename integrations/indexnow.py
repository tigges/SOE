"""IndexNow — push changed URLs to Bing, Yandex, Seznam, Naver etc. (Google does not use IndexNow).

Env: INDEXNOW_KEY — 8-128 chars of a-z, A-Z, 0-9 or '-' (e.g. `python -c "import uuid;print(uuid.uuid4().hex)"`).
Optional INDEXNOW_URL_TXT — full URL (or path) of the key file. Default keyLocation is <site.url>/<key>.txt.
The key must be served as plain text (file content == key) at keyLocation, otherwise the endpoint answers 403.
A 202 means "received, key validation pending".

Wix note: many Wix sites cannot host arbitrary files at the root. If a key file is reachable
(e.g. /indexnow.txt), IndexNow still runs. Otherwise the endpoint answers 403 — use Bing Webmaster Tools.

Not included in run_all (it is a write action). Run explicitly:
    python -m integrations.indexnow configs/<slug>.yaml <outdir>
or from code: run(cfg, outdir, urls=[...]) to submit specific URLs.
Docs: https://www.indexnow.org/documentation
"""
import re
from urllib.parse import urlparse

import requests

from ._common import UA, cli, env, http_error, skip, write_json

NAME = "indexnow"
ENDPOINT = "https://api.indexnow.org/indexnow"
CAP = 10000
CODES = {200: "ok", 202: "accepted, key validation pending", 400: "bad request", 403: "key not valid / key file not found",
         422: "URLs don't belong to host or key mismatch", 429: "too many requests"}


def sitemap_urls(url, s, depth=0, out=None):
    """All <loc> URLs from a sitemap, following sitemap indexes (depth <= 3)."""
    out = [] if out is None else out
    if depth > 3 or len(out) >= CAP:
        return out
    try:
        r = s.get(url, timeout=30)
    except requests.RequestException:
        return out
    if not r.ok:
        return out
    locs = [l.strip() for l in re.findall(r"<loc>\s*(.*?)\s*</loc>", r.text, re.S)]
    locs = [l.replace("&amp;", "&") for l in locs]
    if "<sitemapindex" in r.text:
        for l in locs:
            sitemap_urls(l, s, depth + 1, out)
    else:
        out.extend(locs)
    return out[:CAP]


def key_location(base, key, override=None):
    """URL of the hosted key file. override is INDEXNOW_URL_TXT (full URL or path)."""
    loc = (override or "").strip()
    if not loc or loc == key or re.fullmatch(r"[A-Za-z0-9-]{8,128}", loc):
        return f"{base.rstrip('/')}/{key}.txt"
    if re.match(r"^https?://", loc, re.I):
        return loc
    return f"{base.rstrip('/')}/{loc.lstrip('/')}"


def resolve_key():
    """INDEXNOW_KEY, or the key stored in INDEXNOW_URL_TXT, or the filename of that URL."""
    key, loc = env("INDEXNOW_KEY"), env("INDEXNOW_URL_TXT")
    if key:
        return key, loc
    if not loc:
        return None, None
    if re.fullmatch(r"[A-Za-z0-9-]{8,128}", loc):
        return loc, None
    if re.match(r"^https?://", loc, re.I):
        fname = urlparse(loc).path.rsplit("/", 1)[-1]
        stem = fname[:-4] if fname.lower().endswith(".txt") else fname
        if re.fullmatch(r"[A-Za-z0-9-]{8,128}", stem):
            return stem, loc
    return None, loc


def site_hosts(host):
    h = (host or "").lower()
    apex = h[4:] if h.startswith("www.") else h
    return {h, apex, "www." + apex}


def rewrite_to_host(url, host):
    """Keep same-site URLs; force https + the config host (www vs apex)."""
    p = urlparse(url)
    if p.netloc.lower() not in site_hosts(host):
        return None
    return p._replace(netloc=host, scheme="https").geturl()


def hosted_key_location(session, base, key, override=None):
    """Prefer a URL whose file contents equal the key (default {key}.txt, then /indexnow.txt)."""
    guessed = key_location(base, key, override)
    p = urlparse(base)
    origins = [f"{p.scheme}://{h}" for h in site_hosts(p.netloc)]
    candidates = [guessed]
    for origin in origins:
        candidates += [f"{origin}/indexnow.txt", f"{origin}/{key}.txt"]
    for c in dict.fromkeys(candidates):
        try:
            r = session.get(c, timeout=20)
        except requests.RequestException:
            continue
        if r.ok and (r.text or "").strip() == key:
            return c
    return guessed


def run(cfg: dict, outdir: str, urls=None) -> dict | None:
    key, loc_override = resolve_key()
    if not key:
        return skip(NAME, "INDEXNOW_KEY not set (or put the key / key-file URL in INDEXNOW_URL_TXT)")
    if not re.fullmatch(r"[A-Za-z0-9-]{8,128}", key):
        return {"error": "INDEXNOW_KEY must be 8-128 chars of a-z, A-Z, 0-9, '-'"}
    base = cfg["site"]["url"].rstrip("/")
    host = urlparse(base).netloc
    s = requests.Session()
    s.headers["User-Agent"] = UA
    loc = hosted_key_location(s, base, key, loc_override)
    wix = (cfg.get("site") or {}).get("platform", "").lower() == "wix"
    if wix:
        print("[indexnow] Wix: submitting if a key file is hosted at keyLocation")
    if urls is None:
        urls = sitemap_urls(base + "/sitemap.xml", s) or sitemap_urls(base + "/sitemap_index.xml", s)
    urls = [u for u in (rewrite_to_host(u, host) for u in urls) if u]
    urls = list(dict.fromkeys(urls))[:CAP]
    if not urls:
        urls = [base + "/"]
    body = {"host": host, "key": key, "keyLocation": loc, "urlList": urls}
    try:
        r = s.post(ENDPOINT, json=body, timeout=60,
                   headers={"Content-Type": "application/json; charset=utf-8"})
    except requests.RequestException as e:
        return http_error(e)
    summary = {"submitted": len(urls), "status": r.status_code, "meaning": CODES.get(r.status_code, r.reason),
               "key_location": body["keyLocation"]}
    if r.status_code not in (200, 202):
        summary["error"] = f"HTTP {r.status_code}: {CODES.get(r.status_code, r.text[:200])}"
    write_json(outdir, NAME, {"request": dict(body, key="***"), "response": r.text[:2000], "summary": summary})
    return summary


if __name__ == "__main__":
    cli(run, NAME)

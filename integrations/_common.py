"""Shared helpers for the key-gated integrations (requests only)."""
import datetime as dt, json, os, sys
from urllib.parse import urlparse

import requests

UA = "Mozilla/5.0 (compatible; SOE-Audit/1.0; +https://example.com/soe)"
TIMEOUT = 60


def env(*names):
    """First non-empty env var among names, else None."""
    for n in names:
        v = os.environ.get(n, "").strip()
        if v:
            return v
    return None


def skip(name, reason):
    print(f"[{name}] skipped: {reason}")
    return None


def host(cfg, strip_www=False):
    h = urlparse(cfg["site"]["url"]).netloc.lower()
    return h[4:] if strip_www and h.startswith("www.") else h


def all_keywords(cfg, cap=None):
    kw = cfg.get("keywords") or {}
    out, seen = [], set()
    for k in (kw.get("primary") or []) + (kw.get("secondary") or []):
        if k and k.lower() not in seen:
            seen.add(k.lower())
            out.append(k)
    return out[:cap] if cap else out


def http_error(resp_or_exc):
    """Compact error dict from a Response or a RequestException."""
    if isinstance(resp_or_exc, requests.Response):
        r = resp_or_exc
        try:
            body = r.json()
            msg = (body.get("error") or {}).get("message") if isinstance(body.get("error"), dict) else body
        except ValueError:
            msg = r.text[:300]
        return {"error": f"HTTP {r.status_code}: {msg}"}
    return {"error": f"{type(resp_or_exc).__name__}: {resp_or_exc}"}


def write_json(outdir, name, data):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    return path


def today():
    return dt.date.today()


def google_session(json_path_or_token, scopes, name):
    """Authorised requests session for Google APIs.

    json_path_or_token: path to a service-account JSON file, or a raw OAuth access token.
    google-auth is imported lazily and only needed for the service-account path.
    """
    if os.path.isfile(json_path_or_token):
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import AuthorizedSession
        except ImportError as e:
            raise RuntimeError(f"[{name}] google-auth is not installed: pip install google-auth ({e})")
        creds = service_account.Credentials.from_service_account_file(json_path_or_token, scopes=scopes)
        s = AuthorizedSession(creds)
    else:
        s = requests.Session()
        s.headers["Authorization"] = f"Bearer {json_path_or_token}"
    s.headers["User-Agent"] = UA
    return s


def cli(run, name):
    """`python -m integrations.<name> configs/x.yaml outdir`"""
    import yaml
    if len(sys.argv) < 3:
        sys.exit(f"usage: python -m integrations.{name} configs/<slug>.yaml <outdir>")
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    res = run(cfg, sys.argv[2])
    if res is not None:
        print(json.dumps(res, indent=2, default=str))

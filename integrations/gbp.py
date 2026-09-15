"""Google Business Profile — reviews (My Business v4) + Business Performance daily metrics (last 28 days).

IMPORTANT: GBP APIs are gated. Request access via the GBP API contact form
(https://developers.google.com/my-business/content/prereqs); until Google approves the Cloud project,
calls return 403 / quota 0. Enable "My Business Account Management", "My Business Business Information",
"Business Profile Performance" and the (v4) "Google My Business API" in that project.

Env (one of):
  GBP_CLIENT_ID + GBP_CLIENT_SECRET + GBP_REFRESH_TOKEN
                            recommended for scheduled runs: a long-lived OAuth refresh token (see CONNECT.md);
                            a fresh access token is minted on every run
  GBP_SERVICE_ACCOUNT_JSON  path to a service-account key file (needs google-auth; the service account
                            must itself have access to the profile, which GBP rarely allows — OAuth is usual)
  GBP_OAUTH_TOKEN           an OAuth 2.0 access token with scope https://www.googleapis.com/auth/business.manage
                            (e.g. from OAuth Playground as a profile owner/manager; expires after ~1 hour)
Config: cfg.business.gbp_account ("accounts/123"), cfg.business.gbp_location ("locations/456").
Docs: https://developers.google.com/my-business/reference/rest/v4/accounts.locations.reviews/list
      https://developers.google.com/my-business/reference/performance/rest/v1/locations/fetchMultiDailyMetricsTimeSeries
"""
import datetime as dt
import os

import requests

from ._common import cli, env, google_session, http_error, skip, today, write_json

NAME = "gbp"
SCOPES = ["https://www.googleapis.com/auth/business.manage"]
METRICS = ["CALL_CLICKS", "WEBSITE_CLICKS", "BUSINESS_DIRECTION_REQUESTS",
           "BUSINESS_IMPRESSIONS_MOBILE_MAPS", "BUSINESS_IMPRESSIONS_MOBILE_SEARCH"]
STARS = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5}


def _get(s, url, params):
    try:
        r = s.get(url, params=params, timeout=60)
    except requests.RequestException as e:
        return None, http_error(e)
    return (r.json(), None) if r.ok else (None, http_error(r))


def reviews(s, account, location):
    loc_id = location.split("/")[-1]
    url = f"https://mybusiness.googleapis.com/v4/{account}/locations/{loc_id}/reviews"
    raw, err = _get(s, url, {"pageSize": 50, "orderBy": "updateTime desc"})
    if err:
        return err, None
    revs = [{"stars": STARS.get(r.get("starRating")), "created": r.get("createTime"),
             "reviewer": (r.get("reviewer") or {}).get("displayName"),
             "comment": (r.get("comment") or "")[:280], "replied": bool(r.get("reviewReply"))}
            for r in raw.get("reviews", [])]
    return {"average_rating": raw.get("averageRating"), "total_reviews": raw.get("totalReviewCount"),
            "recent_count": len(revs), "recent_unreplied": sum(not r["replied"] for r in revs),
            "recent": revs}, raw


def performance(s, location):
    end = today() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=27)
    params = [("dailyMetrics", m) for m in METRICS]
    for pre, d in (("dailyRange.start_date", start), ("dailyRange.end_date", end)):
        params += [(f"{pre}.year", d.year), (f"{pre}.month", d.month), (f"{pre}.day", d.day)]
    loc = "locations/" + location.split("/")[-1]
    raw, err = _get(s, f"https://businessprofileperformance.googleapis.com/v1/{loc}:fetchMultiDailyMetricsTimeSeries",
                    params)
    if err:
        return err, None
    totals = {m: 0 for m in METRICS}
    for multi in raw.get("multiDailyMetricTimeSeries", []):
        for ts in multi.get("dailyMetricTimeSeries", []):
            m = ts.get("dailyMetric")
            for dv in (ts.get("timeSeries") or {}).get("datedValues", []):
                totals[m] = totals.get(m, 0) + int(dv.get("value", 0) or 0)  # value is int64-as-string; absent = 0
    return {"start": start.isoformat(), "end": end.isoformat(), "totals": totals}, raw


def refreshed_token():
    """Exchange GBP_REFRESH_TOKEN for a short-lived access token (None if not configured)."""
    cid, secret, refresh = env("GBP_CLIENT_ID"), env("GBP_CLIENT_SECRET"), env("GBP_REFRESH_TOKEN")
    if not (cid and secret and refresh):
        return None
    r = requests.post("https://oauth2.googleapis.com/token", timeout=30,
                      data={"client_id": cid, "client_secret": secret, "refresh_token": refresh,
                            "grant_type": "refresh_token"})
    if not r.ok:
        raise RuntimeError(f"refresh token exchange failed: HTTP {r.status_code} {r.text[:200]}")
    return r.json()["access_token"]


def run(cfg: dict, outdir: str) -> dict | None:
    try:
        token = refreshed_token()
    except Exception as e:
        return {"error": str(e)}
    cred = token or env("GBP_SERVICE_ACCOUNT_JSON", "GBP_OAUTH_TOKEN")
    if not cred:
        return skip(NAME, "GBP_REFRESH_TOKEN (+ client id/secret) / GBP_OAUTH_TOKEN / GBP_SERVICE_ACCOUNT_JSON not set")
    biz = cfg.get("business") or {}
    account, location = biz.get("gbp_account"), biz.get("gbp_location")
    if not (account and location):
        return skip(NAME, "business.gbp_account / business.gbp_location not in config")
    sa = None if token else env("GBP_SERVICE_ACCOUNT_JSON")
    if sa and not os.path.isfile(sa):
        return {"error": f"GBP_SERVICE_ACCOUNT_JSON file not found: {sa}"}
    try:
        s = google_session(cred, SCOPES, NAME)
    except Exception as e:
        return {"error": str(e)}
    summary, raw = {}, {}
    summary["reviews"], raw["reviews"] = reviews(s, account, location)
    summary["performance"], raw["performance"] = performance(s, location)
    if "error" in summary["reviews"] and "error" in summary["performance"]:
        summary["error"] = summary["reviews"]["error"]
    write_json(outdir, NAME, {"raw": raw, "summary": summary})
    if "recent" in summary["reviews"]:  # keep the returned summary compact
        summary["reviews"] = {k: v for k, v in summary["reviews"].items() if k != "recent"}
    return summary


if __name__ == "__main__":
    cli(run, NAME)

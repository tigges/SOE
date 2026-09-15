"""Chrome UX Report (CrUX) API — real-user Core Web Vitals (p75, 28-day rolling), PHONE.

Env: CRUX_API_KEY (or PSI_API_KEY). Key: Google Cloud console > enable "Chrome UX Report API" > Credentials > API key.
Docs: https://developer.chrome.com/docs/crux/api
A 404 ("chrome ux report data not found") means too little Chrome traffic -> {"no_data": true}.
"""
import requests

from ._common import cli, env, http_error, skip, write_json

NAME = "crux"
ENDPOINT = "https://chromeuxreport.googleapis.com/v1/records:queryRecord"
METRICS = {  # name: (good <=, poor >)
    "largest_contentful_paint": (2500, 4000),
    "interaction_to_next_paint": (200, 500),
    "cumulative_layout_shift": (0.1, 0.25),
}


def rate(metric, p75):
    if p75 is None:
        return None
    good, poor = METRICS[metric]
    return "good" if p75 <= good else "poor" if p75 > poor else "ni"


def query(key, **target):
    body = dict(target, formFactor="PHONE", metrics=list(METRICS))
    try:
        r = requests.post(ENDPOINT, params={"key": key}, json=body, timeout=30)
    except requests.RequestException as e:
        return None, http_error(e)
    if r.status_code == 404:
        return None, {"no_data": True}
    if not r.ok:
        return None, http_error(r)
    raw = r.json()
    rec = raw.get("record", {})
    out = {"collection_period": rec.get("collectionPeriod")}
    for m in METRICS:
        p75 = ((rec.get("metrics") or {}).get(m) or {}).get("percentiles", {}).get("p75")
        if p75 is not None:
            p75 = float(p75)  # CLS p75 is a string
        out[m] = {"p75": p75, "rating": rate(m, p75)}
    return raw, out


def run(cfg: dict, outdir: str) -> dict | None:
    key = env("CRUX_API_KEY", "PSI_API_KEY")
    if not key:
        return skip(NAME, "CRUX_API_KEY / PSI_API_KEY not set")
    base = cfg["site"]["url"].rstrip("/")
    raw, summary = {}, {"form_factor": "PHONE"}
    for label, target in (("origin", {"origin": base}), ("homepage", {"url": base + "/"})):
        raw[label], summary[label] = query(key, **target)
    write_json(outdir, NAME, {"raw": raw, "summary": summary})
    return summary


if __name__ == "__main__":
    cli(run, NAME)

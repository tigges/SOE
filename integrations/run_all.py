"""Run every key-gated integration (except IndexNow, which submits URLs) and merge summaries.

    python -m integrations.run_all configs/<slug>.yaml <outdir>
Writes <outdir>/<module>.json per integration and <outdir>/integrations.json with all summaries
(null = skipped for missing credentials).
"""
import datetime as dt
import json
import os
import sys
import traceback

from . import crux, dataforseo, gbp, gsc
from ._common import write_json

MODULES = {"crux": crux, "gsc": gsc, "dataforseo": dataforseo, "gbp": gbp}


def run(cfg: dict, outdir: str) -> dict:
    merged = {"run_at": dt.datetime.now().isoformat(timespec="seconds"), "site": cfg["site"]["url"], "results": {}}
    for name, mod in MODULES.items():
        try:
            merged["results"][name] = mod.run(cfg, outdir)
        except Exception as e:  # one broken integration must not stop the rest
            traceback.print_exc()
            merged["results"][name] = {"error": f"{type(e).__name__}: {e}"}
    # keep a manual Search Console export if the API isn't configured
    exp = os.path.join(outdir, "gsc.json")
    if merged["results"].get("gsc") is None and os.path.exists(exp):
        with open(exp, encoding="utf-8") as f:
            merged["results"]["gsc"] = json.load(f)
    write_json(outdir, "integrations", merged)
    return merged


def main():
    import yaml
    if len(sys.argv) < 3:
        sys.exit("usage: python -m integrations.run_all configs/<slug>.yaml <outdir>")
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    res = run(cfg, sys.argv[2])
    ran = [k for k, v in res["results"].items() if v is not None]
    print(f"integrations: ran {ran or 'none'}; wrote {sys.argv[2]}/integrations.json")
    if ran:
        print(json.dumps({k: res["results"][k] for k in ran}, indent=2, default=str)[:4000])


if __name__ == "__main__":
    main()

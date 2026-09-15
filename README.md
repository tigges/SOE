# SOE template (v2)

A repeatable search optimisation kit for any website. It covers classic search (Google and Bing) and AI answer engines (ChatGPT, Perplexity, Gemini, Google AI Mode).

## The loop in one go

The easiest way to run it is to ask Claude: **`/soe https://example.com`**. To do it by hand:

```bash
pip install requests beautifulsoup4 lxml pyyaml          # + google-auth for Search Console / Business Profile
cp configs/_template.yaml configs/<slug>.yaml            # fill in the settings file
D=reports/<slug>/$(date +%F)
python soe_audit.py configs/<slug>.yaml --out $D --lighthouse --competitors --integrations
python soe_citations.py configs/<slug>.yaml --out $D     # off-site listings
python soe_ai_log.py init configs/<slug>.yaml            # this month's AI-answer rows (fill by hand or with API keys)
python soe_ai_log.py run configs/<slug>.yaml             # auto-fill ChatGPT / Perplexity if keys are set
python soe_ai_log.py summary configs/<slug>.yaml --out $D
python soe_fixes.py configs/<slug>.yaml $D --copy projects/<slug>/copy.yaml   # fix pack
python soe_benchmark.py configs/<slug>.yaml --out $D     # best-in-class leaders: virtual-100 target + feature gaps
python soe_dashboard.py                                  # → dashboard/dist/soe-control-room.html
```

## Dashboard

The SOE Control Room is published with GitHub Pages at **https://tigges.github.io/SOE/**. It's the root `index.html`, rebuilt by `python soe_dashboard.py --standalone --out index.html` and by the "SOE run" Action. `.nojekyll` makes Pages serve it as plain HTML. The page is marked `noindex`, but if the repo is public, anyone with the link can see it.

## What's in the kit

| Path | What it does |
|---|---|
| `PLAYBOOK.md` | The method: six layers, phases, automation tiers, manual checklist |
| `soe_audit.py` | Crawls the site and scores technical, on-page, structured data, name/address/phone, AI readiness and speed. Speed uses the median of 3 Lighthouse runs. Optional flags: `--competitors` (same audit on rival sites), `--integrations` (runs the API modules) |
| `soe_fixes.py` | Fix pack: JSON-LD built from the settings, per-page title/description/H1, platform steps, llms.txt summary, questions to answer |
| `soe_benchmark.py` | Audits the leaders listed under `benchmarks:`. Builds a "virtual 100" from the best leader in each layer, inventories about 40 features on every page, and lists what leaders do that this site doesn't. Features the audit doesn't score yet are flagged as new ideas. `--discover <type> URL…` scores candidate leaders |
| `soe_gsc_import.py` | Imports a Search Console **Performance → Export** zip, so no Google Cloud is needed. Writes `gsc.json`, feeds the dashboard's "Google Search" panel, and keeps the raw CSVs in `data/<site>/gsc/` |
| `soe_citations.py` | Fetches each listing and checks it shows the right name, phone and postcode, flags stale addresses, and lists directories where the site isn't listed yet |
| `soe_ai_log.py` | AI-answer log in `data/<slug>/ai_log.csv`, with monthly rows, API auto-fill and a summary |
| `soe_dashboard.py` + `dashboard/template.html` | Builds the SOE Control Room page from every report |
| `modules/*.yaml` | Rules per site type (local business, SaaS, ecommerce, publisher, personal/artist brand, generic): required schema, expected pages, directory lists |
| `fixpacks/*.yaml` | Step-by-step fixes for Wix, WordPress/Elementor and Next.js, attached to every finding |
| `integrations/` | Key-gated add-ons: CrUX, Search Console, DataForSEO, Business Profile, IndexNow |
| `configs/` · `projects/<slug>/` · `data/<slug>/` | Settings, action plan and approved copy, and the AI log for each site |
| `reports/<slug>/<date>/` | `report.md`, `findings.json`, `competitors.json`, `citations.*`, `ai_visibility.json`, `fixes.*`, `integrations.json` |
| `.github/workflows/soe-run.yml` | **SOE run**: started by hand from GitHub (Actions → SOE run → Run workflow, also in the GitHub mobile app). Choose one site or all, and switch the speed test, competitors and benchmark on or off. It commits the reports and rebuilds the Pages dashboard |

## Keys (all optional; each piece skips cleanly without its key)

**Step-by-step setup: [CONNECT.md](CONNECT.md).** In GitHub Actions, keys are repository secrets. The Search Console key goes in as `GSC_SERVICE_ACCOUNT_B64`, and Business Profile uses `GBP_CLIENT_ID` / `GBP_CLIENT_SECRET` / `GBP_REFRESH_TOKEN`.

| Env var | Unlocks |
|---|---|
| `CRUX_API_KEY` or `PSI_API_KEY` | Real-user Core Web Vitals (free) |
| `GSC_SERVICE_ACCOUNT_JSON` | Search Console clicks, impressions and positions per keyword (free) |
| `OPENAI_API_KEY`, `PERPLEXITY_API_KEY` | Auto-filled AI-answer checks |
| `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` | Organic rank, Maps rank, AI Overview citation and search volume (paid, about £5–20/mo) |
| `GBP_OAUTH_TOKEN` + `business.gbp_account` / `gbp_location` | Business Profile reviews and actions (needs Google approval) |
| `INDEXNOW_KEY` | Pushes changed URLs to Bing and other engines (not possible on Wix) |
| `ANTHROPIC_API_KEY` (+ `SOE_MODEL`) | `soe_fixes.py --llm`: copy drafting inside the GitHub Action |

## Integration details

`integrations/` holds API add-ons. If a module's env vars are not set, it prints `skipped: …` and does nothing else. Each module writes `<outdir>/<name>.json`.

```bash
python -m integrations.run_all configs/<slug>.yaml reports/<slug>/<date>   # all except IndexNow → integrations.json
python -m integrations.crux configs/<slug>.yaml reports/<slug>/<date>      # any single module
```

| Module | Env vars | Setup |
|---|---|---|
| `crux` (real-user Core Web Vitals, phone) | `CRUX_API_KEY` or `PSI_API_KEY` | In Google Cloud, enable the Chrome UX Report API and create an API key under Credentials. |
| `gsc` (Search Console clicks/impressions/positions, 28 days) | `GSC_SERVICE_ACCOUNT_JSON` (path to key file) + `pip install google-auth` | Enable the Search Console API, create a service-account JSON key, and add its e-mail as a user on the property. Set `site.gsc_property` if the property isn't `sc-domain:<host>`. |
| `dataforseo` (organic rank, AI Overview citation, Maps rank, volume) | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | Use the API credentials from app.dataforseo.com/api-access (paid per request, capped at 20 keywords). Optional `site.location`. |
| `gbp` (reviews + calls/clicks/directions/impressions) | `GBP_OAUTH_TOKEN` or `GBP_SERVICE_ACCOUNT_JSON` + `business.gbp_account`, `business.gbp_location` | Google must approve API access first (GBP API access request form). The token needs the `business.manage` scope, e.g. from OAuth Playground. |
| `indexnow` (URL push to Bing/Yandex; not in run_all) | `INDEXNOW_KEY` | Make up an 8–128 char hex key and host it at `<site>/<key>.txt`. This won't work on Wix; submit URLs in Bing Webmaster Tools there instead. |

# Connecting the data sources

Keys never go into files or chat. They live in **GitHub → tigges/SOE → Settings → Secrets and variables → Actions → New repository secret**. The "SOE run" Action reads them from there. After adding keys, start a run: **Actions → SOE run → Run workflow**. That run commits new reports and rebuilds https://tigges.github.io/SOE/.

## You do not have to log into Google Cloud

Most of the kit already works without it:

| Already working / no GCP | How |
|---|---|
| Audit, Lighthouse speed, citations, benchmark, dashboard | Every **SOE run** |
| Copy drafting + Claude AI-answer checks | `ANTHROPIC_API_KEY` (already added) |
| Gemini AI-answer checks | `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) from [Google AI Studio](https://aistudio.google.com/apikey) — not Cloud Console |
| IndexNow (Bing URL ping) | `INDEXNOW_KEY` / `INDEXNOW_URL_TXT` + host a key file on WordPress |
| Search Console | Export Performance as CSV in search.google.com (not cloud.google.com) and import it |
| Google AI Mode / AI Overviews | Monthly check by hand — there is no public API that matches those consumer products |

Google Cloud is only needed if you want these **optional APIs**:

| Optional API | Secret | Hand alternative |
|---|---|---|
| Real-user CrUX / PageSpeed Insights | `CRUX_API_KEY`, `PSI_API_KEY` | Lighthouse already runs; or open https://pagespeed.web.dev |
| Search Console API | `GSC_SERVICE_ACCOUNT_B64` | CSV export (section 2a) |
| Business Profile API | `GBP_CLIENT_ID` / `GBP_CLIENT_SECRET` / `GBP_REFRESH_TOKEN` | Check the profile in Google Maps / Business Profile |

Paid, not Google: DataForSEO (rankings and AI Overviews).

| # | Card on the dashboard | Cost | Time | Secrets |
|---|---|---|---|---|
| 5 | Copy drafting + Claude AI checks | usage | already added | `ANTHROPIC_API_KEY` |
| 5b | Gemini AI-answer checks | usage | already added | `GEMINI_API_KEY` (or `GOOGLE_GEMINI_API_KEY` / `GOOGLE_GENAI_API_KEY` / `GOOGLE_API_KEY`) |
| 6 | IndexNow (Bing URL ping) | free | 5 min + host a file on each WordPress site | `INDEXNOW_KEY`, `INDEXNOW_URL_TXT` |
| 2a | Search Console CSV import | free | 5 min | none |
| 1 | Real-user speed (CrUX) — optional | free | 5 min | `CRUX_API_KEY`, `PSI_API_KEY` |
| 2 | Search Console API — optional | free | 15 min | `GSC_SERVICE_ACCOUNT_B64` |
| 3 | Rankings & AI Overviews | pay as you go | 10 min | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` |
| 4 | Business Profile API — optional | free | Google approval (days–weeks), then 20 min | `GBP_CLIENT_ID`, `GBP_CLIENT_SECRET`, `GBP_REFRESH_TOKEN` |

---

## 0. One Google Cloud project (only if you want CrUX API, GSC API, or Business Profile API)

Skip this section if you are using Lighthouse + GSC CSV + Maps by hand.

1. Go to https://console.cloud.google.com and sign in with charles@tigges.co.uk.
2. In the project picker, choose **New project** and name it `SOE`.

## 1. Real-user speed (CrUX): optional, free

Lab speed already runs (Lighthouse). Use this only for real-user Core Web Vitals.

1. In the SOE project, go to **APIs & Services → Library**. Enable **Chrome UX Report API** and **PageSpeed Insights API**.
2. Go to **APIs & Services → Credentials → Create credentials → API key**.
3. Edit the key: under **API restrictions**, choose *Restrict key* and tick the two APIs above. Save.
4. In GitHub, add the same key twice, as secrets `CRUX_API_KEY` and `PSI_API_KEY`.

Note: small sites often have no real-user data yet. If so, the card shows "No real-user data for this site yet", which is a valid result, not an error. Without a key, check https://pagespeed.web.dev instead.

## 2a. Search Console without Google Cloud (recommended)

1. In https://search.google.com/search-console, open the site, then **Performance → Search results**.
2. Set the date range (e.g. *Last 3 months*), click **Export → Download CSV**. A `.zip` downloads.
3. Import it: `python soe_gsc_import.py configs/<site>.yaml <the .zip>`, or send the zip to Claude.
4. The dashboard's Search Console card and the "Google Search" panel then show impressions, clicks, positions, top searches, pages, countries and plain-English insights. Repeat monthly to build history.

## 2. Search Console via the API (optional, automatic)

1. In the SOE project, enable the **Google Search Console API** in the Library.
2. Go to **IAM & Admin → Service accounts → Create service account**. Name it `soe-reader`; it needs no roles, so click Done.
3. Open the account, then **Keys → Add key → Create new key → JSON**. A `.json` file downloads.
4. Copy the service account's email address (`soe-reader@….iam.gserviceaccount.com`).
5. In https://search.google.com/search-console, for each site:
   - **djurbant.com:** add a **Domain** property `djurbant.com` if it isn't there yet. Verify it with the DNS TXT record at GoDaddy.
   - **yuzuhairandbeauty.london:** the salon's Google account must own the property. Wix can verify it under Marketing & SEO → Get found on Google. Ask the owner to add you as a user, or verify it yourself if you manage the Wix site.
   - Then open **Settings → Users and permissions → Add user**, paste the service-account email, and choose **Restricted** permission.
   - The settings files expect `sc-domain:<domain>`. If you used a URL-prefix property instead, set `site.gsc_property` to e.g. `https://www.yuzuhairandbeauty.london/`.
6. Turn the key file into one line of text and put it on the clipboard (PowerShell; change the file name to match yours):
   ```powershell
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("$HOME\Downloads\soe-xxxx.json")) | Set-Clipboard
   ```
7. In GitHub, add the secret `GSC_SERVICE_ACCOUNT_B64` and paste. Then delete the downloaded `.json` file.

The first data appears 2–3 days after a property is verified.

## 3. Rankings & AI Overviews (DataForSEO): pay as you go

1. Sign up at https://app.dataforseo.com and add funds. The minimum deposit is $50, and it lasts a long time at this volume.
2. Open **API Access**. It shows an **API login** and an **API password**; the password is different from your account password.
3. In GitHub, add the secrets `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`.
4. Each run checks up to 20 keywords per site: Google rank, Maps rank, whether an AI Overview appears and cites the site, and search volume. With today's two sites that's a few cents per run.

Location defaults to London (`site.location` in each settings file).

## 4. Business Profile: optional; needs Google's approval first

You do not need this API to *see* the profile — open it in Google Maps or business.google.com. The API is only for pulling reviews and actions into the dashboard.

You must be an **owner or manager** of the profile. For Yuzu, the salon owner can add you in Business Profile → ⋮ → Business Profile settings → Managers.

1. **Request API access:** https://developers.google.com/my-business/content/prereqs. Use the SOE project number (shown on the project dashboard). Wait for the approval email.
2. **After approval**, enable these APIs in the Library:
   - My Business Account Management API
   - My Business Business Information API
   - Business Profile Performance API
   - Google My Business API
3. **OAuth consent screen** (APIs & Services → OAuth consent screen):
   - Choose External, app name `SOE`, your email.
   - Add yourself as a test user.
   - Then click **Publish app → In production**. While the app is in *Testing*, refresh tokens expire after 7 days. An unverified app is fine for your own use; you'll see a warning screen once.
4. **Credentials → Create credentials → OAuth client ID → Web application.**
   - Add the authorised redirect URI `https://developers.google.com/oauthplayground`.
   - Copy the **Client ID** and **Client secret**.
5. **Get a refresh token**:
   - Open https://developers.google.com/oauthplayground.
   - Click ⚙ and tick *Use your own OAuth credentials*. Paste the client ID and secret.
   - In Step 1, enter the scope `https://www.googleapis.com/auth/business.manage`, then click **Authorize APIs**. Sign in and allow.
   - In Step 2, click **Exchange authorization code for tokens** and copy the **Refresh token**.
6. **Find the profile IDs**, still in the Playground (Step 3, method GET):
   - `https://mybusinessaccountmanagement.googleapis.com/v1/accounts` gives `accounts/<id>`.
   - `https://mybusinessbusinessinformation.googleapis.com/v1/accounts/<id>/locations?readMask=name,title` gives `locations/<id>`.
   - Put both in `configs/yuzu.yaml` as `business.gbp_account` and `business.gbp_location`. These IDs aren't secret.
7. In GitHub, add the secrets `GBP_CLIENT_ID`, `GBP_CLIENT_SECRET` and `GBP_REFRESH_TOKEN`.

## 5. Copy drafting and Claude AI-answer checks: `ANTHROPIC_API_KEY`

Already added. Each **SOE run**:

- calls `soe_fixes.py --llm`, so the Fixes tab titles / descriptions / H1 are Claude drafts (source: "Claude draft")
- calls `soe_ai_log.py run`, which asks Claude (with web search) each prompt in `ai.prompts` and records whether the brand was mentioned or cited

Optional: set `SOE_MODEL` (default `claude-sonnet-4-5`). Perplexity and ChatGPT still auto-fill if you add `PERPLEXITY_API_KEY` / `OPENAI_API_KEY` and list those engines in the site settings.

## 5b. Gemini AI-answer checks: `GEMINI_API_KEY`

This is a **Google AI Studio** key (https://aistudio.google.com/apikey), not a Cloud Console login. The Action also accepts `GOOGLE_GEMINI_API_KEY`, `GOOGLE_GENAI_API_KEY`, or `GOOGLE_API_KEY`.

Each **SOE run** asks Gemini with Google Search grounding and logs mention/citation the same way as Claude. Optional: set `SOE_GEMINI_MODEL` (default `gemini-2.5-flash`).

Google AI Mode / AI Overviews stay a monthly manual check — those consumer products have no matching public API.

## 6. IndexNow (Bing and others): free

Google does not use IndexNow. Wix cannot host the key file, so Yuzu stays on Bing Webmaster Tools.

1. Keep `INDEXNOW_KEY` as 8–128 letters, digits or hyphens (a hex UUID is fine). If the key was stored in `INDEXNOW_URL_TXT` instead, that works too.
2. Host a plain-text file whose **contents equal the key**. Either:
   - `https://<site>/<key>.txt` (the default), or
   - any URL on that host, stored as secret `INDEXNOW_URL_TXT`.
3. WordPress: upload via SFTP (Cloudways → Application → Access details) or a file-manager plugin. The file must be reachable without a login.
4. Re-run **SOE run**. The IndexNow card turns green on a 200/202, or red if the key file is missing (403) or the sitemap is empty.

## Checking it worked

- After **Run workflow** finishes (about 10 minutes), the Connected data cards on https://tigges.github.io/SOE/ turn green or show an error message.
- Each run also writes `reports/<site>/<date>/integrations.json` with what each source returned.
- Ask Claude to "check the SOE run" and it will read the latest reports from the repo.

To test on your own computer, set the same names as environment variables (`$env:CRUX_API_KEY="…"`). Then run:

```powershell
python soe_ai_log.py run configs/yuzu.yaml
python -m integrations.run_all configs/yuzu.yaml reports/test
```

For Search Console locally, use `GSC_SERVICE_ACCOUNT_JSON` with the path to the key file instead of the one-line text version.

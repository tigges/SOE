# SOE Playbook — repeatable search optimisation for any digital project

**Version:** 2.0 (September 2026) · **Status:** running on Yuzu Hair & Beauty (local business, Wix) and DJ UrbanT (artist brand, WordPress)

"Search" now means two things:

- **Classic search:** Google and Bing results pages, plus the map pack.
- **Answer engines:** Google AI Overviews and AI Mode, ChatGPT search, Perplexity, Gemini, Claude.

Being cited in an AI Overview roughly doubles your click-through rate compared with not being cited (Seer Interactive, 2026). Google says AI features have **no extra requirements** beyond normal SEO. So the playbook uses one foundation for both, then adds a GEO layer (generative engine optimisation) that is mostly about *third-party mentions* and *quotable text*.

---

## 1. The model: six layers and a loop

| # | Layer | Question it answers | How it's measured |
|---|---|---|---|
| T | Technical | Can engines crawl and index every important URL? | `soe_audit.py` |
| O | On-page | Does each page clearly target one intent? | `soe_audit.py` |
| S | Structured data | Do machines know what the entity *is*? | `soe_audit.py` + Rich Results Test |
| E | Entity / NAP | Is the business name, address and phone (NAP) identical everywhere, with a strong profile? | script (on-site) + manual (off-site) |
| A | AI search readiness | Can answer engines fetch, understand and quote us? | script + monthly prompt tests |
| P | Performance | Do Core Web Vitals pass? (LCP ≤2.5s, INP ≤200ms, CLS ≤0.1) | Lighthouse / CrUX |
| + | Authority and reputation | Do others mention, link to and review us? | manual / paid tools |

**The loop:**

```
CONFIGURE → AUDIT → PRIORITISE → FIX → PUBLISH/NOTIFY → MEASURE → (monthly) AUDIT again
```

---

## 2. Phases

### Phase 0: Set up (once per project, about 1 hour)

1. Copy `configs/_template.yaml` to `configs/<slug>.yaml`.
2. Fill in the site details, business name/address/phone, 3–5 primary keywords, customer questions, competitors and AI test prompts.
3. Verify the site in **Google Search Console** and **Bing Webmaster Tools**. You can import the Bing site from Search Console.
4. Local businesses only: claim or verify **Google Business Profile**, **Bing Places** and **Apple Business Connect**.
5. Record a baseline:
   - Run `python soe_audit.py configs/<slug>.yaml --lighthouse`.
   - Export Search Console queries (last 3 months).
   - Screenshot results for each AI prompt.

### Phase 1: Foundation fixes (weeks 1–2)

Work through `report.md` from most to least severe:

- **Critical / high:** indexability, blocked bots, missing titles/H1s/descriptions, missing entity schema.
- **Medium:** keyword-to-page mapping, thin pages, content locked in PDFs, llms.txt summary.
- **Low:** alt text, share images, email domain.

### Phase 2: Content and entity (weeks 2–6)

- **One page per money intent.** Each page gets a unique title (keyword + place/brand), one H1, a 140–160 character description, and at least 300 words of *specific* text.
- **Answer content.** Add visible Q&A for the `questions` list. Google removed FAQ rich results in May 2026, but answer engines still quote the text.
- **Entity markup.** Use JSON-LD from `schema/`, with `sameAs` pointing to every profile. It must match the visible content.
- **Prices, menus and specs as HTML**, not PDFs.

### Phase 3: Authority and GEO (ongoing)

- **Reviews:** set a steady monthly target, reply to every review, and ask customers at the moment of delight.
- **Citations and mentions:** get listed in the vertical directories and local and press sources (see §5). "Mentions are the new links" for AI visibility (Whitespark, 2026).
- **Freshness:** post on Google Business Profile and publish short videos/photos regularly. Owner activity and recent video are among the top AI-visibility factors.
- **Change notifications:** ping IndexNow after changes (Bing, Yandex and others) and resubmit sitemaps.

### Phase 4: Measure (monthly)

| Metric | Source | Automatable? |
|---|---|---|
| SOE score and findings diff | `findings.json` | ✅ script / GitHub Action |
| Impressions, clicks, average position per keyword | Search Console API | ✅ free |
| Core Web Vitals (real users) | CrUX API / PageSpeed Insights (key) | ✅ free |
| Business Profile calls, directions, website clicks | Business Profile Performance API (needs access approval) | ⚠️ after approval |
| Map-pack rank grid | DataForSEO / Local Falcon | 💷 paid |
| AI-answer visibility (share of mentions for `ai.prompts`) | Manual screenshot log → Otterly (from $29/mo) or Peec (from €95/mo) | manual → 💷 |
| Reviews: count, rating, velocity | Business Profile Reviews API or manual | ⚠️ |

---

## 3. Automation stack (cheapest first)

| Tier | What | Cost |
|---|---|---|
| 0 | The whole loop (`/soe`, or the "SOE run" GitHub Action, started by hand): audit, competitors, listings, AI log, fix pack, dashboard | free |
| 1 | Add the PSI/CrUX API key and the Search Console API (service account) → keyword and Core Web Vitals trend | free |
| 2 | IndexNow ping on deploy; Bing Webmaster API | free |
| 3 | DataForSEO for rankings and local grids (about $0.60 per 1,000 standard-queue results) | ~£5–20/mo per site |
| 4 | AI-visibility tracker (Otterly / Peec / Semrush AI toolkit) | £25–100/mo |
| 5 | Claude writes `projects/<slug>/copy.yaml` (titles, descriptions, H1s); `soe_fixes.py` merges it with the JSON-LD and platform steps | included |

**Human-in-the-loop rule:** the script finds issues and drafts fixes; a person approves anything published.

---

## 3a. Benchmark against best-in-class leaders

Local competitors show where you stand. **Leaders** show what "great" looks like, and they are where new tactics come from.

1. **Find leaders:** run `soe_benchmark.py --discover <type> URL…` on 10–15 well-known sites in the category and keep the top 2–3 under `benchmarks:`. Leaders don't need to be local.
2. **Target:** the *virtual 100* is the best leader score in each layer. Real sites land at 80–90 on this audit, so the composite is the 100 to aim for.
3. **Gaps:** features at least two leaders use that the site lacks come first. Rows marked **new idea** are tactics the audit doesn't score yet.
4. **Learn:** when a new idea proves useful across several sites, promote it to a check in `soe_audit.py`. The template improves every time it's used.
5. **Review:** refresh the leader list each quarter; leaders change.

## 3b. Which script covers which step

| Step | Script / file |
|---|---|
| Configure | `configs/<slug>.yaml` (drafted by `/soe`) + `modules/<type>.yaml` |
| Audit | `soe_audit.py --lighthouse --competitors --integrations` |
| Benchmark | `soe_benchmark.py` (leaders, virtual 100, new ideas) |
| Listings | `soe_citations.py` |
| AI answers | `soe_ai_log.py init / run / summary` |
| Fix | `soe_fixes.py --copy projects/<slug>/copy.yaml` + `fixpacks/<platform>.yaml` |
| Notify | `integrations/indexnow.py` |
| Measure | `soe_dashboard.py` → SOE Control Room; "SOE run" Action on demand |

## 4. Manual checklist (layers the script can't see)

- [ ] Business Profile: primary category correct, all services listed, hours (including holidays), 10+ recent photos, posts in the last 14 days, booking link
- [ ] Business name, address and phone identical on site, Business Profile, Bing, Apple, Facebook, Instagram, the booking platform and directories
- [ ] Old or duplicate listings and old domains found and fixed or redirected
- [ ] Reviews: count, rating, last 30 days, reply rate
- [ ] Competitors: review count and rating, categories, what they rank for
- [ ] AI prompt test: is the brand mentioned or cited? Which sources are cited instead? (Those are the citation targets.)
- [ ] Backlinks and mentions: local press, business-improvement district, suppliers and brand partners

## 5. Vertical modules

Pick the one that matches `site.type`:

- **local_business:** `LocalBusiness` subtype schema, the Business Profile stack, UK citations (Yell, Thomson Local, Scoot, Cylex, FreeIndex, Hotfrog, Yelp, Nextdoor, Foursquare, the local business-improvement district), plus vertical directories (for salons: Treatwell, Fresha, Booksy, hairdressr).
- **saas:** `Organization` + `SoftwareApplication`; comparison and alternatives pages; docs indexability; G2/Capterra reviews; developer-community mentions.
- **ecommerce:** `Product`/`Offer`/`Review`; Merchant Center feed (this also feeds AI Mode); faceted-navigation crawl control.
- **publisher / personal_brand:** `Article`/`Person`/`MusicGroup`; author pages; `sameAs` to Wikidata, Spotify, SoundCloud and similar; video (YouTube) as a citation source.

## 6. Platform notes

- **Wix:**
  - SEO panel per page (title, description, canonical, robots) and SEO Settings per page type.
  - Custom JSON-LD: up to 5 blocks per page, 7,000 characters each.
  - Redirect manager and robots.txt editor are built in.
  - llms.txt is auto-generated; editing it stops the auto-updates.
  - No server logs.
  - Heavy JavaScript hurts INP/LCP, so remove unused apps.
- **WordPress:**
  - Yoast or Rank Math handle titles, schema and sitemaps.
  - WP Rocket or LiteSpeed for speed; Cloudways page caching.
  - Check that the Cloudflare/WAF bot settings don't block AI crawlers.
- **Next.js / custom:**
  - `generateMetadata`, `app/sitemap.ts`, `robots.ts`.
  - JSON-LD in a layout.
  - Server-render key text.
  - IndexNow on deploy.

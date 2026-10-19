# SOE audit — https://botstudio.uk/

Site: https://botstudio.uk · Run: 2026-10-19 19:28 · Pages crawled: 1 · Sitemap URLs: 0

## Score: 79/100

| Layer | Score |
|---|---|
| Technical | 74 |
| On-page | 80 |
| Structured data | 40 |
| Entity / NAP | 96 |
| AI search readiness | 91 |
| Performance | 96 |

Lighthouse (mobile lab): performance 96, accessibility 95, best-practices 100, seo 91 · LCP 2.3s · TBT 0ms · CLS 0.00

Schema types found: none
AI bots blocked: {'search': [], 'training': []} · llms.txt: True

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| critical | S | schema-missing | none of ['LocalBusiness', 'HairSalon', 'BeautySalon']… found (found: none) | Add JSON-LD for LocalBusiness (see schema/ templates) | / |
| high | T | host-canonicalisation | http://botstudio.uk/ ends at http://botstudio.uk/ | 301 all variants to https://botstudio.uk/ | / |
| high | T | host-canonicalisation | https://www.botstudio.uk/ ends at https://www.botstudio.uk/ | 301 all variants to https://botstudio.uk/ | / |
| high | T | host-canonicalisation | http://www.botstudio.uk/ ends at http://www.botstudio.uk/ | 301 all variants to https://botstudio.uk/ | / |
| high | T | sitemap | no URLs found in /sitemap.xml | Generate an XML sitemap and submit it in GSC/Bing | / |
| high | A | js-only-links | only the homepage could be crawled: internal links aren't in the HTML | Render navigation and key content server-side so crawlers and AI bots can follow links | / |
| medium | O | title-length | 9 chars: 'BotStudio' | Aim for 30–60 chars: primary keyword + location/brand | / |
| medium | O | thin-content | 151 words (<300) | Expand with useful, specific text (services, FAQs, proof) | / |
| medium | O | expected-page | no 'prices' page found (looked for: price, pricing, menu, rates) | Add a dedicated prices page and link it from the navigation | / |
| medium | O | expected-page | no 'services' page found (looked for: service, treatment, balayage, colour) | Add a dedicated services page and link it from the navigation | / |
| medium | O | expected-page | no 'contact' page found (looked for: contact, find-us, location) | Add a dedicated contact page and link it from the navigation | / |
| medium | O | expected-page | no 'about/team' page found (looked for: about, team, stylist, our-story) | Add a dedicated about/team page and link it from the navigation | / |
| medium | E | brand-name | canonical name 'https://botstudio.uk/' not used consistently (title: 'BotStudio') | Use one exact business name everywhere (site, GBP, directories, schema) | / |
| low | T | robots-sitemap | robots.txt does not declare the sitemap | Add 'Sitemap: <url>' | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | / |

## How to fix on wordpress

- **schema-missing** — Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **host-canonicalisation** — Settings → General (WordPress Address + Site Address), plus Cloudways → Domain Management → primary domain and force-HTTPS.
- **sitemap** — Yoast → Settings → Site features → XML sitemaps on. Submit /sitemap_index.xml in Search Console and Bing.
- **title-length** — Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **thin-content** — Add sections in Elementor; Yoast readability/word count helps.
- **expected-page** — Pages → Add New (Elementor), then add it to Appearance → Menus.
- **brand-name** — Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **og-image** — Yoast → Social → Facebook image (1200×630). A site default is in Yoast → Settings → Site basics.

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | BotStudio | ✓ | 1 | 151 |  |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

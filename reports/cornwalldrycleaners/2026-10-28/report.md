# SOE audit — https://cornwalldrycleaners.com/

Site: https://cornwalldrycleaners.com · Run: 2026-10-28 18:53 · Pages crawled: 4 · Sitemap URLs: 4

## Score: 74/100

| Layer | Score |
|---|---|
| Technical | 100 |
| On-page | 48 |
| Structured data | 40 |
| Entity / NAP | 96 |
| AI search readiness | 98 |
| Performance | 62 |

Lighthouse (mobile lab): performance 62, accessibility 100, best-practices 100, seo 92 · LCP 11.1s · TBT 0ms · CLS 0.00

Schema types found: AggregateRating, DryCleaningOrLaundry, GeoCoordinates, OpeningHoursSpecification, PostalAddress
AI bots blocked: {'search': [], 'training': []} · llms.txt: False

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| critical | S | schema-missing | none of ['LocalBusiness', 'HairSalon', 'BeautySalon']… found (found: ['AggregateRating', 'DryCleaningOrLaundry', 'GeoCoordinates', 'OpeningHoursSpecification', 'PostalAddress']) | Add JSON-LD for LocalBusiness (see schema/ templates) | / |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | / |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /2026/10/18/hello-world/ |
| high | O | placeholder-text | template placeholder text on page: 'Hello world!' | Replace builder placeholder copy with real content (it looks unfinished to people and engines) | /2026/10/18/hello-world/ |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /category/uncategorized/ |
| high | O | placeholder-text | template placeholder text on page: 'Hello world!' | Replace builder placeholder copy with real content (it looks unfinished to people and engines) | /category/uncategorized/ |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /author/charles/ |
| high | O | placeholder-text | template placeholder text on page: 'Hello world!' | Replace builder placeholder copy with real content (it looks unfinished to people and engines) | /author/charles/ |
| high | P | lcp | lab LCP 11.1s (good ≤2.5s) | Compress/preload hero image, cut render-blocking JS | / |
| medium | O | thin-content | 63 words (<300) | Expand with useful, specific text (services, FAQs, proof) | /2026/10/18/hello-world/ |
| medium | O | thin-content | 63 words (<300) | Expand with useful, specific text (services, FAQs, proof) | /category/uncategorized/ |
| medium | O | thin-content | 63 words (<300) | Expand with useful, specific text (services, FAQs, proof) | /author/charles/ |
| medium | O | expected-page | no 'prices' page found (looked for: price, pricing, menu, rates) | Add a dedicated prices page and link it from the navigation | / |
| medium | O | expected-page | no 'contact' page found (looked for: contact, find-us, location) | Add a dedicated contact page and link it from the navigation | / |
| medium | O | expected-page | no 'about/team' page found (looked for: about, team, stylist, our-story) | Add a dedicated about/team page and link it from the navigation | / |
| medium | S | schema-sameAs | 'sameAs' not present in any JSON-LD on the site | Include sameAs in the main entity markup | / |
| medium | E | brand-name | canonical name 'https://cornwalldrycleaners.com/' not used consistently (title: 'Cornwall Dry Cleaners – Ealing') | Use one exact business name everywhere (site, GBP, directories, schema) | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | /2026/10/18/hello-world/ |
| low | O | og-image | no og:image | Set a share image (1200×630) | /category/uncategorized/ |
| low | O | og-image | no og:image | Set a share image (1200×630) | /author/charles/ |
| low | A | llms.txt | missing | Optional: publish /llms.txt (cheap, low evidence of impact) | / |

## How to fix on wordpress

- **schema-missing** — Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **meta-description** — Yoast/Rank Math panel → Meta description.
- **placeholder-text** — Search the Elementor templates and pages for the demo text and replace it with real copy.
- **lcp** — Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **thin-content** — Add sections in Elementor; Yoast readability/word count helps.
- **expected-page** — Pages → Add New (Elementor), then add it to Appearance → Menus.
- **schema-sameAs** — Yoast → Settings → Site representation → Other profiles.
- **brand-name** — Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **og-image** — Yoast → Social → Facebook image (1200×630). A site default is in Yoast → Settings → Site basics.
- **llms.txt** — Yoast (v25+) and Rank Math can generate llms.txt, or upload a file to the web root via SFTP (Cloudways → Application → Access details).

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | Cornwall Dry Cleaners – Ealing | ✗ | 1 | 560 | AggregateRating, DryCleaningOrLaundry, GeoCoordinates, OpeningHoursSpecification, PostalAddress |
| /2026/10/18/hello-world/ | Hello world! – Cornwall Dry Cleaners | ✗ | 1 | 63 |  |
| /category/uncategorized/ | Uncategorized – Cornwall Dry Cleaners | ✗ | 1 | 63 |  |
| /author/charles/ | Charles – Cornwall Dry Cleaners | ✗ | 1 | 63 |  |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

# SOE audit — Set Radar

Site: https://www.setradar.ai · Run: 2026-09-16 15:45 · Pages crawled: 20 · Sitemap URLs: 4485

## Score: 75/100

| Layer | Score |
|---|---|
| Technical | 87 |
| On-page | 57 |
| Structured data | 40 |
| Entity / NAP | 96 |
| AI search readiness | 98 |
| Performance | 75 |

Lighthouse (mobile lab): performance 75, accessibility 91, best-practices 79, seo 100 · LCP 15.9s · TBT 46ms · CLS 0.00

Schema types found: none
AI bots blocked: {'search': [], 'training': []} · llms.txt: False

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| critical | S | schema-missing | none of ['Organization', 'Corporation']… found (found: none) | Add JSON-LD for Organization (see schema/ templates) | / |
| critical | S | schema-missing | none of ['SoftwareApplication', 'WebApplication', 'Product']… found (found: none) | Add JSON-LD for SoftwareApplication (see schema/ templates) | / |
| high | T | host-canonicalisation | http://www.setradar.ai/ ends at http://www.setradar.ai/ | 301 all variants to https://www.setradar.ai/ | / |
| high | T | host-canonicalisation | http://setradar.ai/ ends at http://www.setradar.ai/ | 301 all variants to https://www.setradar.ai/ | / |
| high | O | noindex | page is noindex but linked/in sitemap | Remove noindex or drop from sitemap | /stats |
| high | P | lcp | lab LCP 15.9s (good ≤2.5s) | Compress/preload hero image, cut render-blocking JS | / |
| medium | O | title-length | 16 chars: 'Timed tracklists' | Aim for 30–60 chars: primary keyword + location/brand | / |
| medium | O | title-length | 18 chars: 'Sets — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /sets |
| medium | O | title-length | 17 chars: 'DJs — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /djs |
| medium | O | title-length | 20 chars: 'Events — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /events |
| medium | O | title-length | 22 chars: 'Calendar — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /events/calendar |
| medium | O | title-length | 19 chars: 'Atlas — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /atlas |
| medium | O | title-length | 19 chars: 'Stats — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /stats |
| medium | O | title-length | 19 chars: 'About — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /about |
| medium | O | thin-content | 186 words (<250) | Expand with useful, specific text (services, FAQs, proof) | /about |
| medium | O | title-length | 22 chars: 'Wishlist — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /wishlist |
| medium | O | title-length | 20 chars: 'Search — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /search |
| medium | O | thin-content | 42 words (<250) | Expand with useful, specific text (services, FAQs, proof) | /search |
| medium | O | title-length | 20 chars: 'Labels — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /labels |
| medium | O | title-length | 20 chars: 'Tracks — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /tracks |
| medium | O | title-length | 68 chars: 'PAWSA LIVE @ SPACE MIAMI 🇺🇸 SOLID GROOVES MMW 25.03.22 — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /sets/sc-pawsa-pawsa-live-space-miami-solid-grooves-mmw-250322 |
| medium | O | title-length | 79 chars: 'PAWSA LIVE @ BROOKLYN, NEW YORK, SUPERIOR INGREDIENTS 🇺🇸 10.04.22 — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /sets/sc-pawsa-pawsa-live-superior-ingredients-brooklyn-new-york-100422 |
| medium | O | title-length | 73 chars: 'PAWSA LIVE @ CIRCOLOCO, FABRIKA, RIO DE JANEIRO 🇧🇷 21.04.22 — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /sets/sc-pawsa-pawsa-live-circoloco-fabrika-rio-de-janeiro-210422 |
| medium | O | title-length | 81 chars: 'PAWSA LIVE @ PRINTWORKS, LONDON 🇬🇧 SOLID GROOVES 10TH BIRTHDAY 2022 — setradar.ai' | Aim for 30–60 chars: primary keyword + location/brand | /sets/sc-pawsa-pawsa-live-printworks-london |
| medium | O | expected-page | no 'pricing' page found (looked for: pricing, plans) | Add a dedicated pricing page and link it from the navigation | / |
| medium | O | expected-page | no 'docs' page found (looked for: docs, documentation, developers, help) | Add a dedicated docs page and link it from the navigation | / |
| medium | O | expected-page | no 'integrations' page found (looked for: integration, apps, marketplace) | Add a dedicated integrations page and link it from the navigation | / |
| medium | O | keyword-targeting | primary keyword 'festival setlist' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | O | keyword-targeting | primary keyword 'Set Radar' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | E | brand-name | canonical name 'Set Radar' not used consistently (title: 'Timed tracklists') | Use one exact business name everywhere (site, GBP, directories, schema) | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | /sets |
| low | O | og-image | no og:image | Set a share image (1200×630) | /djs |
| low | O | og-image | no og:image | Set a share image (1200×630) | /events |
| low | O | og-image | no og:image | Set a share image (1200×630) | /events/calendar |
| low | O | h1 | 2 H1s | Use one H1 per page | /atlas |
| low | O | og-image | no og:image | Set a share image (1200×630) | /atlas |
| low | O | og-image | no og:image | Set a share image (1200×630) | /stats |
| low | O | og-image | no og:image | Set a share image (1200×630) | /about |
| low | O | og-image | no og:image | Set a share image (1200×630) | /wishlist |
| low | O | og-image | no og:image | Set a share image (1200×630) | /search |
| low | O | og-image | no og:image | Set a share image (1200×630) | /labels |
| low | O | og-image | no og:image | Set a share image (1200×630) | /tracks |
| low | A | llms.txt | missing | Optional: publish /llms.txt (cheap, low evidence of impact) | / |

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | Timed tracklists | ✓ | 1 | 260 |  |
| /sets | Sets — setradar.ai | ✓ | 1 | 721 |  |
| /djs | DJs — setradar.ai | ✓ | 1 | 3339 |  |
| /events | Events — setradar.ai | ✓ | 1 | 1221 |  |
| /events/calendar | Calendar — setradar.ai | ✓ | 1 | 1798 |  |
| /atlas | Atlas — setradar.ai | ✓ | 2 | 2055 |  |
| /stats | Stats — setradar.ai | ✓ | 1 | 2646 |  |
| /about | About — setradar.ai | ✓ | 1 | 186 |  |
| /wishlist | Wishlist — setradar.ai | ✓ | 1 | 348 |  |
| /search | Search — setradar.ai | ✓ | 1 | 42 |  |
| /labels | Labels — setradar.ai | ✓ | 1 | 6700 |  |
| /tracks | Tracks — setradar.ai | ✓ | 1 | 1645 |  |
| /sets/sc-pawsa-pawsa-live-solid-grooves-island-london-2021 | PAWSA live @ Solid Grooves Island London 2021 — setradar.ai | ✓ | 1 | 482 |  |
| /sets/sc-pawsa-pawsa-live-cocorico-riccione-041221 | PAWSA LIVE @ COCORICÒ, RICCIONE 🇮🇹 04.12.21 — setradar.ai | ✓ | 1 | 626 |  |
| /sets/sc-sammyvirji-valentines-mixtape | Valentine's Mixtape — setradar.ai | ✓ | 1 | 559 |  |
| /sets/sc-pawsa-pawsa-live-space-miami-solid-grooves-mmw-250322 | PAWSA LIVE @ SPACE MIAMI 🇺🇸 SOLID GROOVES MMW 25.03.22 — setradar.ai | ✓ | 1 | 625 |  |
| /sets/sc-pawsa-pawsa-live-superior-ingredients-brooklyn-new-york-100422 | PAWSA LIVE @ BROOKLYN, NEW YORK, SUPERIOR INGREDIENTS 🇺🇸 10.04.22 — setradar.ai | ✓ | 1 | 741 |  |
| /sets/sc-pawsa-pawsa-live-circoloco-fabrika-rio-de-janeiro-210422 | PAWSA LIVE @ CIRCOLOCO, FABRIKA, RIO DE JANEIRO 🇧🇷 21.04.22 — setradar.ai | ✓ | 1 | 456 |  |
| /sets/sc-pawsa-pawsa-live-printworks-london | PAWSA LIVE @ PRINTWORKS, LONDON 🇬🇧 SOLID GROOVES 10TH BIRTHDAY 2022 — setradar.ai | ✓ | 1 | 498 |  |
| /sets/sc-pawsa-pawsa-live-circoloco-dc10-ibiza | PAWSA LIVE @ CIRCOLOCO DC10 IBIZA 2022 — setradar.ai | ✓ | 1 | 479 |  |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

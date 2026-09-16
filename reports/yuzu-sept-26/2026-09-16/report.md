# SOE audit — Yuzu Hair & Beauty (Sept 26)

Site: https://tigges.github.io/YUZU_SEPT_26 · Run: 2026-09-16 13:43 · Pages crawled: 6 · Sitemap URLs: 7

## Score: 95/100

| Layer | Score |
|---|---|
| Technical | 87 |
| On-page | 96 |
| Structured data | 100 |
| Entity / NAP | 98 |
| AI search readiness | 100 |
| Performance | 92 |

Lighthouse (mobile lab): performance 92, accessibility 95, best-practices 100, seo 100 · LCP 2.8s · TBT 9ms · CLS 0.00

Schema types found: Answer, FAQPage, GeoCoordinates, HairSalon, OpeningHoursSpecification, PostalAddress, Question, ReserveAction
AI bots blocked: {'search': [], 'training': []} · llms.txt: True

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| high | T | host-canonicalisation | http://tigges.github.io/ ends at http://tigges.github.io/ | 301 all variants to https://tigges.github.io/YUZU_SEPT_26/ | / |
| high | T | host-canonicalisation | http://www.tigges.github.io/ ends at http://www.tigges.github.io/ | 301 all variants to https://tigges.github.io/YUZU_SEPT_26/ | / |
| medium | O | content-in-pdf | 2 PDF(s) linked site-wide — key info (e.g. prices) may be locked in PDF | Publish that content as HTML (crawlable, quotable by AI); keep PDF as a download | /patch-testing.pdf |
| medium | P | lcp | lab LCP 2.8s (good ≤2.5s) | Compress/preload hero image, cut render-blocking JS | / |
| low | E | email-domain | email info@yuzuhairandbeauty.co.uk is on a different domain from the site | Use an address on the site domain, or redirect the old domain to the site | / |

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | Hair Salon Ealing Broadway / Yuzu Hair & Beauty | ✓ | 1 | 303 | GeoCoordinates, HairSalon, OpeningHoursSpecification, PostalAddress, ReserveAction |
| /services.html | Hair Salon Services in Ealing / Yuzu Hair | ✓ | 1 | 341 | GeoCoordinates, HairSalon, OpeningHoursSpecification, PostalAddress |
| /prices.html | Hair Price List Ealing Broadway / Yuzu Hair | ✓ | 1 | 338 | GeoCoordinates, HairSalon, OpeningHoursSpecification, PostalAddress, ReserveAction |
| /contact.html | Contact the Hairdresser Ealing Broadway | ✓ | 1 | 322 | GeoCoordinates, HairSalon, OpeningHoursSpecification, PostalAddress |
| /about.html | About the Team at Yuzu Hair Ealing | ✓ | 1 | 321 | GeoCoordinates, HairSalon, OpeningHoursSpecification, PostalAddress, ReserveAction |
| /questions.html | Questions at the Hair Salon in Ealing | ✓ | 1 | 329 | Answer, FAQPage, GeoCoordinates, HairSalon, OpeningHoursSpecification, PostalAddress, Question, ReserveAction |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

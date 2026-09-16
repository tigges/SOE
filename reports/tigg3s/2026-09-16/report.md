# SOE audit — www.tigg3s.com

Site: https://www.tigg3s.com · Run: 2026-09-16 12:51 · Pages crawled: 1 · Sitemap URLs: 1

## Score: 90/100

| Layer | Score |
|---|---|
| Technical | 84 |
| On-page | 90 |
| Structured data | 100 |
| Entity / NAP | 96 |
| AI search readiness | 100 |
| Performance | 73 |

Lighthouse (mobile lab): performance 73, accessibility 100, best-practices 100, seo 100 · LCP 5.1s · TBT 0ms · CLS 0.00

Schema types found: Answer, FAQPage, Organization, Person, Question, WebSite
AI bots blocked: {'search': [], 'training': []} · llms.txt: True

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| high | T | host-canonicalisation | http://www.tigg3s.com/ ends at http://tigg3s.com/ | 301 all variants to https://www.tigg3s.com/ | / |
| high | T | host-canonicalisation | https://tigg3s.com/ ends at https://tigg3s.com/ | 301 all variants to https://www.tigg3s.com/ | / |
| high | T | host-canonicalisation | http://tigg3s.com/ ends at http://tigg3s.com/ | 301 all variants to https://www.tigg3s.com/ | / |
| high | P | lcp | lab LCP 5.1s (good ≤2.5s) | Compress/preload hero image, cut render-blocking JS | / |
| medium | O | canonical | points to https://tigg3s.com/ | Self-reference unless intentional | / |
| medium | O | expected-page | no 'contact/booking' page found (looked for: contact, booking, press) | Add a dedicated contact/booking page and link it from the navigation | / |
| medium | E | brand-name | canonical name 'www.tigg3s.com' not used consistently (title: 'TIGGES — Family and ventures hub') | Use one exact business name everywhere (site, GBP, directories, schema) | / |
| low | O | alt-text | 1/2 images lack alt | Describe images; include service/location naturally | / |

## How to fix on wordpress

- **host-canonicalisation** — Settings → General (WordPress Address + Site Address), plus Cloudways → Domain Management → primary domain and force-HTTPS.
- **lcp** — Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **canonical** — Yoast → Advanced → Canonical URL.
- **expected-page** — Pages → Add New (Elementor), then add it to Appearance → Menus.
- **brand-name** — Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **alt-text** — Media Library → image → Alternative Text.

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | TIGGES — Family and ventures hub | ✓ | 1 | 300 | Answer, FAQPage, Organization, Person, Question, WebSite |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

# SOE audit — Art Barbara

Site: https://barbaratigges.com · Run: 2026-09-16 15:44 · Pages crawled: 2 · Sitemap URLs: 6

## Score: 77/100

| Layer | Score |
|---|---|
| Technical | 100 |
| On-page | 71 |
| Structured data | 40 |
| Entity / NAP | 96 |
| AI search readiness | 82 |
| Performance | 70 |

Lighthouse (mobile lab): performance 70, accessibility 99, best-practices 100, seo 92 · LCP 53.1s · TBT 0ms · CLS 0.00

Schema types found: none
AI bots blocked: {'search': [], 'training': []} · llms.txt: True

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| critical | S | schema-missing | none of ['Person', 'MusicGroup', 'Organization']… found (found: none) | Add JSON-LD for Person (see schema/ templates) | / |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | / |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /studio/ |
| high | A | extractable-text | homepage has 142 words of text | AI answers quote text: add concise factual paragraphs (who/what/where/price/hours) | / |
| high | P | lcp | lab LCP 53.1s (good ≤2.5s) | Compress/preload hero image, cut render-blocking JS | / |
| medium | O | thin-content | 142 words (<200) | Expand with useful, specific text (services, FAQs, proof) | / |
| medium | O | thin-content | 27 words (<200) | Expand with useful, specific text (services, FAQs, proof) | /studio/ |
| medium | O | expected-page | no 'events' page found (looked for: event, gig, tour, dates) | Add a dedicated events page and link it from the navigation | / |
| medium | O | expected-page | no 'contact/booking' page found (looked for: contact, booking, press) | Add a dedicated contact/booking page and link it from the navigation | / |
| medium | E | brand-name | canonical name 'Art Barbara' not used consistently (title: 'https://barbaratigges.com – Art aus Basel') | Use one exact business name everywhere (site, GBP, directories, schema) | / |
| medium | A | llms.txt-summary | summary does not mention ['painting'] | Rewrite the llms.txt summary to describe the business, not a random page | / |
| medium | A | answer-content | no question-style content found | Add an FAQ / Q&A section answering real customer questions (visible text, not just schema) | / |
| low | O | alt-text | 1/21 images lack alt | Describe images; include service/location naturally | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | /studio/ |

## How to fix on wordpress

- **schema-missing** — Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **meta-description** — Yoast/Rank Math panel → Meta description.
- **lcp** — Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **thin-content** — Add sections in Elementor; Yoast readability/word count helps.
- **expected-page** — Pages → Add New (Elementor), then add it to Appearance → Menus.
- **brand-name** — Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **llms.txt-summary** — Edit the llms.txt summary in the plugin or in the file.
- **answer-content** — Add an FAQ section (Elementor Accordion). It's visible text for AI answers; FAQ rich results no longer show.
- **alt-text** — Media Library → image → Alternative Text.
- **og-image** — Yoast → Social → Facebook image (1200×630). A site default is in Yoast → Settings → Site basics.

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | https://barbaratigges.com – Art aus Basel | ✗ | 1 | 142 |  |
| /studio/ | Studio – https://barbaratigges.com | ✗ | 1 | 27 |  |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

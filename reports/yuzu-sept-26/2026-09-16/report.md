# SOE audit — Yuzu Hair & Beauty (Sept 26)

Site: https://tigges.github.io/YUZU_SEPT_26 · Run: 2026-09-16 12:07 · Pages crawled: 1 · Sitemap URLs: 0

## Score: 70/100

| Layer | Score |
|---|---|
| Technical | 74 |
| On-page | 68 |
| Structured data | 40 |
| Entity / NAP | 78 |
| AI search readiness | 76 |
| Performance | 85 |

Lighthouse (mobile lab): performance 85, accessibility 95, best-practices 96, seo 100 · LCP 4.0s · TBT 0ms · CLS 0.06

Schema types found: none
AI bots blocked: {'search': [], 'training': []} · llms.txt: False

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| critical | S | schema-missing | none of ['LocalBusiness', 'HairSalon', 'BeautySalon']… found (found: none) | Add JSON-LD for LocalBusiness (see schema/ templates) | / |
| high | T | host-canonicalisation | http://tigges.github.io/ ends at http://tigges.github.io/ | 301 all variants to https://tigges.github.io/YUZU_SEPT_26/ | / |
| high | T | host-canonicalisation | http://www.tigges.github.io/ ends at http://www.tigges.github.io/ | 301 all variants to https://tigges.github.io/YUZU_SEPT_26/ | / |
| high | T | sitemap | no URLs found in /sitemap.xml | Generate an XML sitemap and submit it in GSC/Bing | / |
| high | O | h1 | no H1 | Add exactly one descriptive H1 containing the primary topic | / |
| high | A | js-only-links | only the homepage could be crawled: internal links aren't in the HTML | Render navigation and key content server-side so crawlers and AI bots can follow links | / |
| high | E | nap-phone | configured phone not found on site | Show the phone in the footer on every page | / |
| high | E | nap-postcode | postcode not found on site | Show the full address in the footer | / |
| high | A | extractable-text | homepage has 0 words of text | AI answers quote text: add concise factual paragraphs (who/what/where/price/hours) | / |
| medium | T | robots.txt | missing | Publish robots.txt with Sitemap: line | / |
| medium | O | thin-content | 0 words (<300) | Expand with useful, specific text (services, FAQs, proof) | / |
| medium | O | expected-page | no 'prices' page found (looked for: price, pricing, menu, rates) | Add a dedicated prices page and link it from the navigation | / |
| medium | O | expected-page | no 'services' page found (looked for: service, treatment, balayage, colour) | Add a dedicated services page and link it from the navigation | / |
| medium | O | expected-page | no 'contact' page found (looked for: contact, find-us, location) | Add a dedicated contact page and link it from the navigation | / |
| medium | O | expected-page | no 'about/team' page found (looked for: about, team, stylist, our-story) | Add a dedicated about/team page and link it from the navigation | / |
| medium | O | keyword-targeting | primary keyword 'hair salon Ealing' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | O | keyword-targeting | primary keyword 'hairdresser Ealing Broadway' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | O | keyword-targeting | primary keyword 'Japanese hair salon London' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | A | answer-content | no question-style content found | Add an FAQ / Q&A section answering real customer questions (visible text, not just schema) | / |
| medium | P | lcp | lab LCP 4.0s (good ≤2.5s) | Compress/preload hero image, cut render-blocking JS | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | / |
| low | E | email-domain | email info@yuzuhairandbeauty.co.uk is on a different domain from the site | Use an address on the site domain, or redirect the old domain to the site | / |
| low | E | profile-link | instagram profile not linked from site | Link profiles and add them to schema sameAs | / |
| low | E | profile-link | facebook profile not linked from site | Link profiles and add them to schema sameAs | / |
| low | E | profile-link | booking profile not linked from site | Link profiles and add them to schema sameAs | / |
| low | E | profile-link | tiktok profile not linked from site | Link profiles and add them to schema sameAs | / |
| low | A | llms.txt | missing | Optional: publish /llms.txt (cheap, low evidence of impact) | / |

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | Yuzu Hair & Beauty · Ealing Broadway | ✓ | 0 | 0 |  |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

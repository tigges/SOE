# SOE audit — TIGGES

Site: https://tigg3s.com · Run: 2026-09-16 15:43 · Pages crawled: 2 · Sitemap URLs: 2

## Score: 92/100

| Layer | Score |
|---|---|
| Technical | 87 |
| On-page | 81 |
| Structured data | 100 |
| Entity / NAP | 100 |
| AI search readiness | 91 |
| Performance | 95 |

Lighthouse (mobile lab): performance 95, accessibility 100, best-practices 100, seo 100 · LCP 2.9s · TBT 0ms · CLS 0.00

Schema types found: AboutPage, Answer, FAQPage, Organization, Person, Question, WebSite
AI bots blocked: {'search': [], 'training': []} · llms.txt: True

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| high | T | host-canonicalisation | http://tigg3s.com/ ends at http://tigg3s.com/ | 301 all variants to https://tigg3s.com/ | / |
| high | T | host-canonicalisation | http://www.tigg3s.com/ ends at http://tigg3s.com/ | 301 all variants to https://tigg3s.com/ | / |
| high | A | extractable-text | homepage has 56 words of text | AI answers quote text: add concise factual paragraphs (who/what/where/price/hours) | / |
| medium | O | thin-content | 56 words (<250) | Expand with useful, specific text (services, FAQs, proof) | / |
| medium | O | thin-content | 237 words (<250) | Expand with useful, specific text (services, FAQs, proof) | /about.html |
| medium | O | expected-page | no 'contact/booking' page found (looked for: contact, booking, press) | Add a dedicated contact/booking page and link it from the navigation | / |
| medium | O | keyword-targeting | primary keyword 'Tigges family' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | O | keyword-targeting | primary keyword 'DJ URBANT' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | P | lcp | lab LCP 2.9s (good ≤2.5s) | Compress/preload hero image, cut render-blocking JS | / |
| low | O | alt-text | 1/2 images lack alt | Describe images; include service/location naturally | / |

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | TIGGES — Family and ventures hub | ✓ | 1 | 56 | Organization, Person, WebSite |
| /about.html | About TIGGES — Family and ventures | ✓ | 1 | 237 | AboutPage, Answer, FAQPage, Question |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

# SOE audit — www.tigg3s.com

Site: https://www.tigg3s.com · Run: 2026-09-16 00:48 · Pages crawled: 1 · Sitemap URLs: 0

## Score: 72/100

| Layer | Score |
|---|---|
| Technical | 71 |
| On-page | 72 |
| Structured data | 40 |
| Entity / NAP | 96 |
| AI search readiness | 76 |
| Performance | 79 |

Lighthouse (mobile lab): performance 79, accessibility 100, best-practices 100, seo 100 · LCP 5.1s · TBT 0ms · CLS 0.00

Schema types found: none
AI bots blocked: {'search': [], 'training': []} · llms.txt: False

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| critical | S | schema-missing | none of ['Person', 'MusicGroup', 'Organization']… found (found: none) | Add JSON-LD for Person (see schema/ templates) | / |
| high | T | host-canonicalisation | http://www.tigg3s.com/ ends at http://tigg3s.com/ | 301 all variants to https://www.tigg3s.com/ | / |
| high | T | host-canonicalisation | https://tigg3s.com/ ends at https://tigg3s.com/ | 301 all variants to https://www.tigg3s.com/ | / |
| high | T | host-canonicalisation | http://tigg3s.com/ ends at http://tigg3s.com/ | 301 all variants to https://www.tigg3s.com/ | / |
| high | T | sitemap | no URLs found in /sitemap.xml | Generate an XML sitemap and submit it in GSC/Bing | / |
| high | O | h1 | no H1 | Add exactly one descriptive H1 containing the primary topic | / |
| high | A | js-only-links | only the homepage could be crawled: internal links aren't in the HTML | Render navigation and key content server-side so crawlers and AI bots can follow links | / |
| high | A | extractable-text | homepage has 0 words of text | AI answers quote text: add concise factual paragraphs (who/what/where/price/hours) | / |
| high | P | lcp | lab LCP 5.1s (good ≤2.5s) | Compress/preload hero image, cut render-blocking JS | / |
| medium | T | robots.txt | missing | Publish robots.txt with Sitemap: line | / |
| medium | O | title-length | 6 chars: 'Tigges' | Aim for 30–60 chars: primary keyword + location/brand | / |
| medium | O | thin-content | 0 words (<300) | Expand with useful, specific text (services, FAQs, proof) | / |
| medium | O | expected-page | no 'about/bio' page found (looked for: about, bio) | Add a dedicated about/bio page and link it from the navigation | / |
| medium | O | expected-page | no 'music/work' page found (looked for: music, mixes, releases, work) | Add a dedicated music/work page and link it from the navigation | / |
| medium | O | expected-page | no 'events' page found (looked for: event, gig, tour, dates) | Add a dedicated events page and link it from the navigation | / |
| medium | O | expected-page | no 'contact/booking' page found (looked for: contact, booking, press) | Add a dedicated contact/booking page and link it from the navigation | / |
| medium | E | brand-name | canonical name 'www.tigg3s.com' not used consistently (title: 'Tigges') | Use one exact business name everywhere (site, GBP, directories, schema) | / |
| medium | A | answer-content | no question-style content found | Add an FAQ / Q&A section answering real customer questions (visible text, not just schema) | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | / |
| low | A | llms.txt | missing | Optional: publish /llms.txt (cheap, low evidence of impact) | / |

## How to fix on wordpress

- **schema-missing** — Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **host-canonicalisation** — Settings → General (WordPress Address + Site Address), plus Cloudways → Domain Management → primary domain and force-HTTPS.
- **sitemap** — Yoast → Settings → Site features → XML sitemaps on. Submit /sitemap_index.xml in Search Console and Bing.
- **h1** — Elementor Heading widget → Content → HTML Tag = H1. Make sure the theme isn't also printing the page title as an H1 (Elementor → Page settings → Hide title).
- **lcp** — Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **robots.txt** — Yoast → Tools → File editor, or upload robots.txt to the web root.
- **title-length** — Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **thin-content** — Add sections in Elementor; Yoast readability/word count helps.
- **expected-page** — Pages → Add New (Elementor), then add it to Appearance → Menus.
- **brand-name** — Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **answer-content** — Add an FAQ section (Elementor Accordion). It's visible text for AI answers; FAQ rich results no longer show.
- **og-image** — Yoast → Social → Facebook image (1200×630). A site default is in Yoast → Settings → Site basics.
- **llms.txt** — Yoast (v25+) and Rank Math can generate llms.txt, or upload a file to the web root via SFTP (Cloudways → Application → Access details).

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | Tigges | ✓ | 0 | 0 |  |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

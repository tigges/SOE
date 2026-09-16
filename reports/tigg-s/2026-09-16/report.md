# SOE audit — TIGG3S.com

Site: https://www.TIGG£S.com · Run: 2026-09-16 00:42 · Pages crawled: 0 · Sitemap URLs: 0

## Score: 0/100

| Layer | Score |
|---|---|
| Technical | 0 |
| On-page | 0 |
| Structured data | 0 |
| Entity / NAP | 0 |
| AI search readiness | 0 |
| Performance | n/a (run with --lighthouse) |

Schema types found: none
AI bots blocked: {'search': [], 'training': []} · llms.txt: False

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| critical | T | homepage | status None | Fix homepage availability | / |
| critical | T | unreachable | no HTML pages could be fetched (site down, blocked or wrong URL) | Check the URL, and that the server/CDN doesn't block normal crawlers | / |
| critical | S | schema-missing | none of ['LocalBusiness', 'HairSalon', 'BeautySalon']… found (found: none) | Add JSON-LD for LocalBusiness (see schema/ templates) | / |
| high | T | sitemap | no URLs found in /sitemap.xml | Generate an XML sitemap and submit it in GSC/Bing | / |
| medium | T | robots.txt | missing | Publish robots.txt with Sitemap: line | / |
| medium | E | brand-name | canonical name 'TIGG3S.com' not used consistently (title: '') | Use one exact business name everywhere (site, GBP, directories, schema) | / |
| medium | A | answer-content | no question-style content found | Add an FAQ / Q&A section answering real customer questions (visible text, not just schema) | / |
| low | A | llms.txt | missing | Optional: publish /llms.txt (cheap, low evidence of impact) | / |

## How to fix on wordpress

- **schema-missing** — Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **sitemap** — Yoast → Settings → Site features → XML sitemaps on. Submit /sitemap_index.xml in Search Console and Bing.
- **robots.txt** — Yoast → Tools → File editor, or upload robots.txt to the web root.
- **brand-name** — Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **answer-content** — Add an FAQ section (Elementor Accordion). It's visible text for AI answers; FAQ rich results no longer show.
- **llms.txt** — Yoast (v25+) and Rank Math can generate llms.txt, or upload a file to the web root via SFTP (Cloudways → Application → Access details).

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

# SOE audit — Yuzu Hair & Beauty

Site: https://www.yuzuhairandbeauty.london · Run: 2026-09-15 08:19 · Pages crawled: 7 · Sitemap URLs: 7

## Score: 72/100

| Layer | Score |
|---|---|
| Technical | 100 |
| On-page | 3 |
| Structured data | 76 |
| Entity / NAP | 92 |
| AI search readiness | 96 |
| Performance | 79 |

Lighthouse (mobile lab): performance 79, accessibility 96, best-practices 79, seo 85 · LCP 2.5s · TBT 693ms · CLS 0.01

Schema types found: ImageObject, WebSite
AI bots blocked: {'search': [], 'training': []} · llms.txt: True

## Findings (most severe first)

| Sev | Layer | Check | Detail | Fix | URL |
|---|---|---|---|---|---|
| critical | S | schema-missing | none of ['LocalBusiness', 'HairSalon', 'BeautySalon']… found (found: ['ImageObject', 'WebSite']) | Add JSON-LD for LocalBusiness (see schema/ templates) | / |
| high | O | title-quality | spaced/all-caps title 'H O M E / Yuzu Hair' | Use a readable keyword title, not a design label | / |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | / |
| high | O | h1 | no H1 | Add exactly one descriptive H1 containing the primary topic | / |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /items/senior-stylists |
| high | O | placeholder-text | template placeholder text on page: 'This is placeholder text' | Replace builder placeholder copy with real content (it looks unfinished to people and engines) | /items/senior-stylists |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /items/stylists |
| high | O | placeholder-text | template placeholder text on page: 'This is placeholder text' | Replace builder placeholder copy with real content (it looks unfinished to people and engines) | /items/stylists |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /items/models |
| high | O | placeholder-text | template placeholder text on page: 'This is placeholder text' | Replace builder placeholder copy with real content (it looks unfinished to people and engines) | /items/models |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /o-f-f-e-r-s-1 |
| high | O | h1 | no H1 | Add exactly one descriptive H1 containing the primary topic | /o-f-f-e-r-s-1 |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /terms-and-conditions |
| high | O | h1 | no H1 | Add exactly one descriptive H1 containing the primary topic | /terms-and-conditions |
| high | O | meta-description | missing | Write a 140–160 char description with a call to action | /items |
| medium | O | title-length | 19 chars: 'H O M E / Yuzu Hair' | Aim for 30–60 chars: primary keyword + location/brand | / |
| medium | O | thin-content | 255 words (<300) | Expand with useful, specific text (services, FAQs, proof) | / |
| medium | O | thin-content | 248 words (<300) | Expand with useful, specific text (services, FAQs, proof) | /items/senior-stylists |
| medium | O | title-length | 20 chars: 'Stylists / Yuzu Hair' | Aim for 30–60 chars: primary keyword + location/brand | /items/stylists |
| medium | O | thin-content | 254 words (<300) | Expand with useful, specific text (services, FAQs, proof) | /items/stylists |
| medium | O | title-length | 18 chars: 'Models / Yuzu Hair' | Aim for 30–60 chars: primary keyword + location/brand | /items/models |
| medium | O | thin-content | 264 words (<300) | Expand with useful, specific text (services, FAQs, proof) | /items/models |
| medium | O | title-length | 18 chars: 'OFFERS / Yuzu Hair' | Aim for 30–60 chars: primary keyword + location/brand | /o-f-f-e-r-s-1 |
| medium | O | title-length | 24 chars: 'Items (List) / Yuzu Hair' | Aim for 30–60 chars: primary keyword + location/brand | /items |
| medium | O | thin-content | 156 words (<300) | Expand with useful, specific text (services, FAQs, proof) | /items |
| medium | O | content-in-pdf | 2 PDF(s) linked site-wide — key info (e.g. prices) may be locked in PDF | Publish that content as HTML (crawlable, quotable by AI); keep PDF as a download | /_files/ugd/4ea19e_5ad90785107649c5a308c57cf4f4e75f.pdf |
| medium | O | expected-page | no 'services' page found (looked for: service, treatment, balayage, colour) | Add a dedicated services page and link it from the navigation | / |
| medium | O | keyword-targeting | primary keyword 'hair salon Ealing' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | O | keyword-targeting | primary keyword 'hairdresser Ealing Broadway' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | O | keyword-targeting | primary keyword 'Japanese hair salon London' not in homepage title/H1 | Map each primary keyword to one page and use it in title + H1 | / |
| medium | S | schema-openingHoursSpecification | 'openingHoursSpecification' not present in any JSON-LD on the site | Include openingHoursSpecification in the main entity markup | / |
| medium | S | schema-sameAs | 'sameAs' not present in any JSON-LD on the site | Include sameAs in the main entity markup | / |
| medium | E | brand-name | canonical name 'Yuzu Hair & Beauty' not used consistently (title: 'H O M E / Yuzu Hair') | Use one exact business name everywhere (site, GBP, directories, schema) | / |
| medium | A | llms.txt-summary | summary does not mention ['Ealing'] | Rewrite the llms.txt summary to describe the business, not a random page | / |
| medium | P | tbt-inp-proxy | TBT 693ms (INP risk) | Remove unused apps/widgets and third-party scripts | / |
| low | O | alt-text | 2/11 images lack alt | Describe images; include service/location naturally | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | / |
| low | O | og-image | no og:image | Set a share image (1200×630) | /o-f-f-e-r-s-1 |
| low | O | og-image | no og:image | Set a share image (1200×630) | /terms-and-conditions |
| low | O | og-image | no og:image | Set a share image (1200×630) | /items |
| low | E | email-domain | email info@yuzuhairandbeauty.co.uk is on a different domain from the site | Use an address on the site domain, or redirect the old domain to the site | / |
| low | E | profile-link | tiktok profile not linked from site | Link profiles and add them to schema sameAs | / |

## How to fix on wix

- **schema-missing** — Pages & Menu → page ⋯ → SEO → Advanced SEO → Structured data markup → Add new markup. Paste JSON-LD (max 7,000 chars, up to 5 per page) and check it in the Rich Results Test.
- **title-quality** — Editor → Pages & Menu → page ⋯ → SEO basics → Title tag. For many pages at once: Dashboard → Marketing & SEO → SEO → SEO Settings → page type → edit the title pattern.
- **meta-description** — Pages & Menu → page ⋯ → SEO basics → Meta description. The SEO Settings page-type pattern is the fallback.
- **h1** — Select the main heading → Edit text → Semantic tag = Heading 1 (H1). Use only one per page. For spaced lettering, use letter spacing, not spaces typed between letters.
- **placeholder-text** — Open the page (or the CMS collection item in Content Manager) and replace the default Wix text. Check dynamic item pages too.
- **title-length** — Editor → Pages & Menu → page ⋯ → SEO basics → Title tag. For many pages at once: Dashboard → Marketing & SEO → SEO → SEO Settings → page type → edit the title pattern.
- **thin-content** — Add text sections in the Editor (a Text + Image strip). Wix gives no word count, so re-run the audit afterwards.
- **content-in-pdf** — Rebuild the PDF content as a Wix page (or use Wix Bookings service/price lists). Keep the PDF as a download link.
- **expected-page** — Pages & Menu → + Add page. Also add it to the menu so it's linked.
- **keyword-targeting** — Put the keyword in the title tag (SEO basics) and in the page's main heading. In the Editor, select the heading text → Text settings → Semantic tag = H1.
- **schema-openingHoursSpecification** — Pages & Menu → page ⋯ → SEO → Advanced SEO → Structured data markup → Add new markup. Paste JSON-LD (max 7,000 chars, up to 5 per page) and check it in the Rich Results Test.
- **schema-sameAs** — Pages & Menu → page ⋯ → SEO → Advanced SEO → Structured data markup → Add new markup. Paste JSON-LD (max 7,000 chars, up to 5 per page) and check it in the Rich Results Test.
- **brand-name** — Settings → Business info → Business name. Then use the same name in titles, the footer and every profile.
- **llms.txt-summary** — Dashboard → SEO → llms.txt → edit the summary paragraph. Once edited it no longer auto-updates.
- **tbt-inp-proxy** — Remove unused apps and third-party embeds; limit animations (Editor → Animations).
- **alt-text** — Click the image → Settings → 'What's in the image? Tell Google' (the alt text).
- **og-image** — Pages & Menu → page ⋯ → Social share → upload a 1200×630 image. The site-wide default is in SEO Settings.

## Pages

| URL | Title | Desc | H1 | Words | Schema |
|---|---|---|---|---|---|
| / | H O M E / Yuzu Hair | ✗ | 0 | 255 | WebSite |
| /items/senior-stylists | Senior Stylists / Yuzu Hair | ✗ | 1 | 248 | ImageObject |
| /items/stylists | Stylists / Yuzu Hair | ✗ | 1 | 254 | ImageObject |
| /items/models | Models / Yuzu Hair | ✗ | 1 | 264 | ImageObject |
| /o-f-f-e-r-s-1 | OFFERS / Yuzu Hair | ✗ | 0 | 438 |  |
| /terms-and-conditions | TERMS AND CONDITIONS / Yuzu Hair | ✗ | 0 | 820 |  |
| /items | Items (List) / Yuzu Hair | ✗ | 1 | 156 |  |

_Manual layers not covered by this script: Google Business Profile, reviews, citations, backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._

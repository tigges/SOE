# Fix pack — www.tigg3s.com

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — have Claude rewrite it (the /soe skill does this) or run with --llm.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://www.tigg3s.com/#entity",
  "name": "www.tigg3s.com",
  "url": "https://www.tigg3s.com/"
}
```

## 2. Page titles, descriptions, H1

| Page | Now | Proposed title | Proposed description | H1 | Source |
|---|---|---|---|---|---|
| https://www.tigg3s.com/ | Tigges | Tigges Family & Ventures \| Personal Brand Portfolio | Explore Tigges family ventures and professional activities. Discover projects, connections, and updates from the Tigges portfolio. Visit now. | Tigges Family & Ventures | Claude draft |

## 3. Steps on wordpress

- **schema-missing** (critical, ×1) — Add JSON-LD for Person (see schema/ templates)  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **host-canonicalisation** (high, ×3) — 301 all variants to https://www.tigg3s.com/  
  _How:_ Settings → General (WordPress Address + Site Address), plus Cloudways → Domain Management → primary domain and force-HTTPS.
- **sitemap** (high, ×1) — Generate an XML sitemap and submit it in GSC/Bing  
  _How:_ Yoast → Settings → Site features → XML sitemaps on. Submit /sitemap_index.xml in Search Console and Bing.
- **h1** (high, ×1) — Add exactly one descriptive H1 containing the primary topic  
  _How:_ Elementor Heading widget → Content → HTML Tag = H1. Make sure the theme isn't also printing the page title as an H1 (Elementor → Page settings → Hide title).
- **js-only-links** (high, ×1) — Render navigation and key content server-side so crawlers and AI bots can follow links
- **extractable-text** (high, ×1) — AI answers quote text: add concise factual paragraphs (who/what/where/price/hours)
- **lcp** (high, ×1) — Compress/preload hero image, cut render-blocking JS  
  _How:_ Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **robots.txt** (medium, ×1) — Publish robots.txt with Sitemap: line  
  _How:_ Yoast → Tools → File editor, or upload robots.txt to the web root.
- **title-length** (medium, ×1) — Aim for 30–60 chars: primary keyword + location/brand  
  _How:_ Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **thin-content** (medium, ×1) — Expand with useful, specific text (services, FAQs, proof)  
  _How:_ Add sections in Elementor; Yoast readability/word count helps.
- **expected-page** (medium, ×4) — Add a dedicated about/bio page and link it from the navigation  
  _How:_ Pages → Add New (Elementor), then add it to Appearance → Menus.
- **brand-name** (medium, ×1) — Use one exact business name everywhere (site, GBP, directories, schema)  
  _How:_ Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **answer-content** (medium, ×1) — Add an FAQ / Q&A section answering real customer questions (visible text, not just schema)  
  _How:_ Add an FAQ section (Elementor Accordion). It's visible text for AI answers; FAQ rich results no longer show.
- **og-image** (low, ×1) — Set a share image (1200×630)  
  _How:_ Yoast → Social → Facebook image (1200×630). A site default is in Yoast → Settings → Site basics.
- **llms.txt** (low, ×1) — Optional: publish /llms.txt (cheap, low evidence of impact)  
  _How:_ Yoast (v25+) and Rank Math can generate llms.txt, or upload a file to the web root via SFTP (Cloudways → Application → Access details).

## 4. llms.txt summary

> www.tigg3s.com


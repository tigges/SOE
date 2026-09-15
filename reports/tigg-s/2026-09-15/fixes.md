# Fix pack — TIGG3S.com

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — have Claude rewrite it (the /soe skill does this) or run with --llm.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://www.TIGG£S.com/#entity",
  "name": "TIGG3S.com",
  "url": "https://www.TIGG£S.com/"
}
```

## 2. Page titles, descriptions, H1

| Page | Now | Proposed title | Proposed description | H1 | Source |
|---|---|---|---|---|---|

## 3. Steps on wordpress

- **homepage** (critical, ×1) — Fix homepage availability
- **unreachable** (critical, ×1) — Check the URL, and that the server/CDN doesn't block normal crawlers
- **schema-missing** (critical, ×1) — Add JSON-LD for LocalBusiness (see schema/ templates)  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **sitemap** (high, ×1) — Generate an XML sitemap and submit it in GSC/Bing  
  _How:_ Yoast → Settings → Site features → XML sitemaps on. Submit /sitemap_index.xml in Search Console and Bing.
- **robots.txt** (medium, ×1) — Publish robots.txt with Sitemap: line  
  _How:_ Yoast → Tools → File editor, or upload robots.txt to the web root.
- **brand-name** (medium, ×1) — Use one exact business name everywhere (site, GBP, directories, schema)  
  _How:_ Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **answer-content** (medium, ×1) — Add an FAQ / Q&A section answering real customer questions (visible text, not just schema)  
  _How:_ Add an FAQ section (Elementor Accordion). It's visible text for AI answers; FAQ rich results no longer show.
- **llms.txt** (low, ×1) — Optional: publish /llms.txt (cheap, low evidence of impact)  
  _How:_ Yoast (v25+) and Rank Math can generate llms.txt, or upload a file to the web root via SFTP (Cloudways → Application → Access details).

## 4. llms.txt summary

> TIGG3S.com


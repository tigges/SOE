# Fix pack — www.tigg3s.com

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — run with --llm (Gemini first, then Claude) or rewrite in a session.

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
| https://www.tigg3s.com/ | TIGGES — Family and ventures hub | TIGGES Family & Ventures Hub \| Art, Music & Tech | Explore the TIGGES family ventures: art, architecture, DJ URBANT music, Set Radar, and GTA VI.AI. Discover our creative projects today. | TIGGES Family and Ventures | Claude draft |

## 3. Steps on wordpress

- **host-canonicalisation** (high, ×3) — 301 all variants to https://www.tigg3s.com/  
  _How:_ Settings → General (WordPress Address + Site Address), plus Cloudways → Domain Management → primary domain and force-HTTPS.
- **lcp** (high, ×1) — Compress/preload hero image, cut render-blocking JS  
  _How:_ Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **canonical** (medium, ×1) — Self-reference unless intentional  
  _How:_ Yoast → Advanced → Canonical URL.
- **expected-page** (medium, ×1) — Add a dedicated contact/booking page and link it from the navigation  
  _How:_ Pages → Add New (Elementor), then add it to Appearance → Menus.
- **brand-name** (medium, ×1) — Use one exact business name everywhere (site, GBP, directories, schema)  
  _How:_ Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **alt-text** (low, ×1) — Describe images; include service/location naturally  
  _How:_ Media Library → image → Alternative Text.

## 4. llms.txt summary

> www.tigg3s.com


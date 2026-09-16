# Fix pack — Art Barbara

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — run with --llm (Gemini first, then Claude) or rewrite in a session.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://barbaratigges.com/#entity",
  "name": "Art Barbara",
  "url": "https://barbaratigges.com/",
  "description": "Barbara Tigges — paintings and works on paper (Basel)."
}
```

## 2. Page titles, descriptions, H1

| Page | Now | Proposed title | Proposed description | H1 | Source |
|---|---|---|---|---|---|
| https://barbaratigges.com/ | https://barbaratigges.com – Art aus Basel | Barbara Tigges \| Art Barbara | Barbara Tigges at Art Barbara. Listen, see upcoming dates and get in touch for bookings. | Barbara Tigges | DRAFT (rule-based) |
| https://barbaratigges.com/studio/ | Studio – https://barbaratigges.com | Studio \| Art Barbara | Studio at Art Barbara in Barbara Tigges. Listen, see upcoming dates and get in touch for bookings. | Studio | DRAFT (rule-based) |

## 3. Steps on wordpress

- **schema-missing** (critical, ×1) — Add JSON-LD for Person (see schema/ templates)  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **meta-description** (high, ×2) — Write a 140–160 char description with a call to action  
  _How:_ Yoast/Rank Math panel → Meta description.
- **extractable-text** (high, ×1) — AI answers quote text: add concise factual paragraphs (who/what/where/price/hours)
- **lcp** (high, ×1) — Compress/preload hero image, cut render-blocking JS  
  _How:_ Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **thin-content** (medium, ×2) — Expand with useful, specific text (services, FAQs, proof)  
  _How:_ Add sections in Elementor; Yoast readability/word count helps.
- **expected-page** (medium, ×2) — Add a dedicated events page and link it from the navigation  
  _How:_ Pages → Add New (Elementor), then add it to Appearance → Menus.
- **brand-name** (medium, ×1) — Use one exact business name everywhere (site, GBP, directories, schema)  
  _How:_ Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **llms.txt-summary** (medium, ×1) — Rewrite the llms.txt summary to describe the business, not a random page  
  _How:_ Edit the llms.txt summary in the plugin or in the file.
- **answer-content** (medium, ×1) — Add an FAQ / Q&A section answering real customer questions (visible text, not just schema)  
  _How:_ Add an FAQ section (Elementor Accordion). It's visible text for AI answers; FAQ rich results no longer show.
- **alt-text** (low, ×1) — Describe images; include service/location naturally  
  _How:_ Media Library → image → Alternative Text.
- **og-image** (low, ×2) — Set a share image (1200×630)  
  _How:_ Yoast → Social → Facebook image (1200×630). A site default is in Yoast → Settings → Site basics.

## 4. llms.txt summary

> Art Barbara Barbara Tigges — paintings and works on paper (Basel).


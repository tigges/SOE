# Fix pack — https://botstudio.uk/

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — run with --llm (Gemini first, then Claude) or rewrite in a session.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://botstudio.uk/#entity",
  "name": "https://botstudio.uk/",
  "url": "https://botstudio.uk/"
}
```

## 2. Page titles, descriptions, H1

| Page | Now | Proposed title | Proposed description | H1 | Source |
|---|---|---|---|---|---|
| https://botstudio.uk/ | BotStudio | BotStudio - Hybrid AI Agent & Bot Building Platform | Build and operate hybrid bot workforces that answer from your content. Your team steps in when needed. Connect AI agents to your business today. | Build, Operate, and Connect Your Hybrid Agent Workforce | Claude draft |

## 3. Steps on wordpress

- **schema-missing** (critical, ×1) — Add JSON-LD for LocalBusiness (see schema/ templates)  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **host-canonicalisation** (high, ×3) — 301 all variants to https://botstudio.uk/  
  _How:_ Settings → General (WordPress Address + Site Address), plus Cloudways → Domain Management → primary domain and force-HTTPS.
- **sitemap** (high, ×1) — Generate an XML sitemap and submit it in GSC/Bing  
  _How:_ Yoast → Settings → Site features → XML sitemaps on. Submit /sitemap_index.xml in Search Console and Bing.
- **js-only-links** (high, ×1) — Render navigation and key content server-side so crawlers and AI bots can follow links
- **title-length** (medium, ×1) — Aim for 30–60 chars: primary keyword + location/brand  
  _How:_ Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **thin-content** (medium, ×1) — Expand with useful, specific text (services, FAQs, proof)  
  _How:_ Add sections in Elementor; Yoast readability/word count helps.
- **expected-page** (medium, ×4) — Add a dedicated prices page and link it from the navigation  
  _How:_ Pages → Add New (Elementor), then add it to Appearance → Menus.
- **brand-name** (medium, ×1) — Use one exact business name everywhere (site, GBP, directories, schema)  
  _How:_ Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **robots-sitemap** (low, ×1) — Add 'Sitemap: <url>'
- **og-image** (low, ×1) — Set a share image (1200×630)  
  _How:_ Yoast → Social → Facebook image (1200×630). A site default is in Yoast → Settings → Site basics.

## 4. llms.txt summary

> https://botstudio.uk/


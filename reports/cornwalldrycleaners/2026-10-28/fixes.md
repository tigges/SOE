# Fix pack — https://cornwalldrycleaners.com/

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — run with --llm (Gemini first, then Claude) or rewrite in a session.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://cornwalldrycleaners.com/#entity",
  "name": "https://cornwalldrycleaners.com/",
  "url": "https://cornwalldrycleaners.com/"
}
```

## 2. Page titles, descriptions, H1

| Page | Now | Proposed title | Proposed description | H1 | Source |
|---|---|---|---|---|---|
| https://cornwalldrycleaners.com/ | Cornwall Dry Cleaners – Ealing | Dry Cleaning Services in Ealing \| Cornwall Dry Cleaners | Trusted dry cleaning and laundry services in Ealing. The dry cleaners neighbours recommend for quality garment care. Contact us today for a quote. | Ealing's Trusted Dry Cleaning Service | Claude draft |
| https://cornwalldrycleaners.com/prices/ |  | Dry Cleaning Prices Ealing \| Cornwall Dry Cleaners | View our competitive dry cleaning and laundry prices in Ealing. Transparent pricing for garments, suits, dresses and more. Get a free quote today. | Our Dry Cleaning Prices | Claude draft |
| https://cornwalldrycleaners.com/contact/ |  | Contact Cornwall Dry Cleaners Ealing \| Get In Touch | Contact Cornwall Dry Cleaners in Ealing for all your garment care needs. Visit us, call or enquire online for dry cleaning and laundry services. | Contact Us in Ealing | Claude draft |
| https://cornwalldrycleaners.com/about/ |  | About Cornwall Dry Cleaners Ealing \| Our Story | Learn about Cornwall Dry Cleaners, Ealing's recommended dry cleaning service. Discover our commitment to quality garment care. Visit us today. | About Cornwall Dry Cleaners | Claude draft |

## 3. Steps on wordpress

- **schema-missing** (critical, ×1) — Add JSON-LD for LocalBusiness (see schema/ templates)  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **meta-description** (high, ×4) — Write a 140–160 char description with a call to action  
  _How:_ Yoast/Rank Math panel → Meta description.
- **placeholder-text** (high, ×3) — Replace builder placeholder copy with real content (it looks unfinished to people and engines)  
  _How:_ Search the Elementor templates and pages for the demo text and replace it with real copy.
- **lcp** (high, ×1) — Compress/preload hero image, cut render-blocking JS  
  _How:_ Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **thin-content** (medium, ×3) — Expand with useful, specific text (services, FAQs, proof)  
  _How:_ Add sections in Elementor; Yoast readability/word count helps.
- **expected-page** (medium, ×3) — Add a dedicated prices page and link it from the navigation  
  _How:_ Pages → Add New (Elementor), then add it to Appearance → Menus.
- **schema-sameAs** (medium, ×1) — Include sameAs in the main entity markup  
  _How:_ Yoast → Settings → Site representation → Other profiles.
- **brand-name** (medium, ×1) — Use one exact business name everywhere (site, GBP, directories, schema)  
  _How:_ Settings → General → Site Title, plus Yoast → Site representation → Organisation name.
- **og-image** (low, ×4) — Set a share image (1200×630)  
  _How:_ Yoast → Social → Facebook image (1200×630). A site default is in Yoast → Settings → Site basics.
- **llms.txt** (low, ×1) — Optional: publish /llms.txt (cheap, low evidence of impact)  
  _How:_ Yoast (v25+) and Rank Math can generate llms.txt, or upload a file to the web root via SFTP (Cloudways → Application → Access details).

## 4. llms.txt summary

> https://cornwalldrycleaners.com/


# Fix pack — DJ UrbanT

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — have Claude rewrite it (the /soe skill does this) or run with --llm.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://djurbant.com/#entity",
  "name": "DJ UrbanT",
  "url": "https://djurbant.com/",
  "description": "DJ UrbanT is a London bass house and tech house DJ; djurbant.com is the brand and booking hub.",
  "sameAs": [
    "https://www.instagram.com/_urbant_/"
  ]
}
```

## 2. Page titles, descriptions, H1

| Page | Now | Proposed title | Proposed description | H1 | Source |
|---|---|---|---|---|---|
| https://djurbant.com/ | DJ UrbanT – Bass House. Tech House. Live Sets. | Bass House DJ London \| DJ UrbanT \| Tech House Sets | DJ UrbanT is a London bass house and tech house DJ. Explore live sets, videos, and audio mixes. Book DJ UrbanT for your event today. | Bass House DJ London \| DJ UrbanT | Claude draft |
| https://djurbant.com/video/ | Video – DJ UrbanT | DJ UrbanT Video \| Live Bass House & Tech House Sets | Watch DJ UrbanT's live bass house and tech house DJ sets. Experience high-energy performances from London's DJ UrbanT. View videos now. | DJ UrbanT Live Video Sets | Claude draft |
| https://djurbant.com/audio/ | Audio – DJ UrbanT | DJ UrbanT Audio \| Bass House & Tech House Mixes | Listen to DJ UrbanT's bass house and tech house audio mixes. Stream exclusive tracks from London DJ UrbanT. Play mixes now. | DJ UrbanT Audio Mixes | Claude draft |
| https://djurbant.com/contact/ | Contact – DJ UrbanT | Book a Bass House DJ \| Contact DJ UrbanT London | Book DJ UrbanT for your event. London-based bass house and tech house DJ available for bookings. Contact DJ UrbanT today for availability. | Book DJ UrbanT | Claude draft |
| https://djurbant.com/map/ | Map – DJ UrbanT | DJ UrbanT Location \| London Bass House DJ Map | Find DJ UrbanT's London location and event coverage areas. Bass house and tech house DJ serving London and surrounding areas. View map now. | DJ UrbanT Location Map | Claude draft |

## 3. Steps on wordpress

- **schema-missing** (critical, ×1) — Add JSON-LD for Person (see schema/ templates)  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **meta-description** (high, ×12) — Write a 140–160 char description with a call to action  
  _How:_ Yoast/Rank Math panel → Meta description.
- **h1** (high, ×4) — Add exactly one descriptive H1 containing the primary topic  
  _How:_ Elementor Heading widget → Content → HTML Tag = H1. Make sure the theme isn't also printing the page title as an H1 (Elementor → Page settings → Hide title).
- **placeholder-text** (high, ×4) — Replace builder placeholder copy with real content (it looks unfinished to people and engines)  
  _How:_ Search the Elementor templates and pages for the demo text and replace it with real copy.
- **noindex** (high, ×3) — Remove noindex or drop from sitemap  
  _How:_ Yoast → Advanced → Allow search engines to show this page = Yes. Also check Settings → Reading → 'Discourage search engines' is off.
- **extractable-text** (high, ×1) — AI answers quote text: add concise factual paragraphs (who/what/where/price/hours)
- **lcp** (high, ×1) — Compress/preload hero image, cut render-blocking JS  
  _How:_ Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **thin-content** (medium, ×12) — Expand with useful, specific text (services, FAQs, proof)  
  _How:_ Add sections in Elementor; Yoast readability/word count helps.
- **title-length** (medium, ×7) — Aim for 30–60 chars: primary keyword + location/brand  
  _How:_ Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **duplicate-title** (medium, ×1) — Make titles unique  
  _How:_ Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **expected-page** (medium, ×2) — Add a dedicated about/bio page and link it from the navigation  
  _How:_ Pages → Add New (Elementor), then add it to Appearance → Menus.
- **keyword-targeting** (medium, ×1) — Map each primary keyword to one page and use it in title + H1  
  _How:_ Set the focus keyphrase in Yoast/Rank Math, and use it in the SEO title and the Elementor heading widget (HTML tag H1).
- **tbt-inp-proxy** (medium, ×1) — Remove unused apps/widgets and third-party scripts  
  _How:_ Defer JS (WP Rocket, Perfmatters or Breeze) and remove unused plugins, sliders and third-party chat widgets.
- **alt-text** (low, ×2) — Describe images; include service/location naturally  
  _How:_ Media Library → image → Alternative Text.
- **og-image** (low, ×12) — Set a share image (1200×630)  
  _How:_ Yoast → Social → Facebook image (1200×630). A site default is in Yoast → Settings → Site basics.
- **llms.txt** (low, ×1) — Optional: publish /llms.txt (cheap, low evidence of impact)  
  _How:_ Yoast (v25+) and Rank Math can generate llms.txt, or upload a file to the web root via SFTP (Cloudways → Application → Access details).

## 4. llms.txt summary

> DJ UrbanT DJ UrbanT is a London bass house and tech house DJ; djurbant.com is the brand and booking hub.

## 5. Q&A block (visible on the page; answers to be written from real facts)

**Who is DJ UrbanT?**  
_Answer: …_
**How do I book DJ UrbanT?**  
_Answer: …_

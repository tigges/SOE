# Fix pack — TIGGES ARCHITEKT

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — run with --llm (Gemini first, then Claude) or rewrite in a session.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://tigges.es/#entity",
  "name": "TIGGES ARCHITEKT",
  "url": "https://tigges.es/",
  "description": "Architecture studio in Spain (Tigges family). tiggesarchitekt.ch redirects here."
}
```

## 2. Page titles, descriptions, H1

| Page | Now | Proposed title | Proposed description | H1 | Source |
|---|---|---|---|---|---|
| https://tigges.es/ | Home - TIGGES ARCHITEKT | Tigges Architekt \| TIGGES ARCHITEKT | Tigges Architekt at TIGGES ARCHITEKT. See prices and opening hours, and book online. | Tigges Architekt | DRAFT (rule-based) |
| https://tigges.es/minergie-sustainability/ | Minergie - TIGGES ARCHITEKT | Minergie \| TIGGES ARCHITEKT | Minergie at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Minergie | DRAFT (rule-based) |
| https://tigges.es/daniel-tigges/ | Daniel Tigges - TIGGES ARCHITEKT | Daniel Tigges \| TIGGES ARCHITEKT | Daniel Tigges at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Daniel Tigges | DRAFT (rule-based) |
| https://tigges.es/es/contacto/ | Contacto - TIGGES ARCHITEKT | Contacto \| TIGGES ARCHITEKT | Contacto at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Contacto | DRAFT (rule-based) |
| https://tigges.es/contact/ | Contact - TIGGES ARCHITEKT | Contact \| TIGGES ARCHITEKT | Contact at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Contact | DRAFT (rule-based) |
| https://tigges.es/es/minergie/ | Minergie - TIGGES ARCHITEKT | Minergie \| TIGGES ARCHITEKT | Minergie at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Minergie | DRAFT (rule-based) |
| https://tigges.es/es/daniel-tigges/ | Daniel Tigges - TIGGES ARCHITEKT | Daniel Tigges \| TIGGES ARCHITEKT | Daniel Tigges at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Daniel Tigges | DRAFT (rule-based) |
| https://tigges.es/es/home/ | Home - TIGGES ARCHITEKT | Home \| TIGGES ARCHITEKT | Home at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Home | DRAFT (rule-based) |
| https://tigges.es/portfolio/historic-building-gets-passivhaus/ | PASSIVHAUS PLUS - TIGGES ARCHITEKT | Passivhaus Plus \| TIGGES ARCHITEKT | Passivhaus Plus at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Passivhaus Plus | DRAFT (rule-based) |
| https://tigges.es/portfolio/goethe-institute/ | GOETHE INSTITUTE - TIGGES ARCHITEKT | Goethe Institute \| TIGGES ARCHITEKT | Goethe Institute at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Goethe Institute | DRAFT (rule-based) |
| https://tigges.es/portfolio/historic-building-gets-efficient-passivhaus-2/ | HISTORIC BUILDING GETS EFFICIENT PASSIVHAUS - TIGGES ARCHITEKT | Historic Building Gets Efficient Passivhaus \| TIGGES ARCHITE | Historic Building Gets Efficient Passivhaus at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Historic Building Gets Efficient Passivhaus | DRAFT (rule-based) |
| https://tigges.es/portfolio/competition-school-mitte-brig/ | COMPETITION SCHOOL BRIG - TIGGES ARCHITEKT | Competition School Brig \| TIGGES ARCHITEKT | Competition School Brig at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Competition School Brig | DRAFT (rule-based) |
| https://tigges.es/portfolio/house-with-pool-alella-neu/ | HOUSE WITH POOL ALELLA - TIGGES ARCHITEKT | House With Pool Alella \| TIGGES ARCHITEKT | House With Pool Alella at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | House With Pool Alella | DRAFT (rule-based) |
| https://tigges.es/portfolio/casa-collsuspina/ | CASA COLLSUSPINA - TIGGES ARCHITEKT | Casa Collsuspina \| TIGGES ARCHITEKT | Casa Collsuspina at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Casa Collsuspina | DRAFT (rule-based) |
| https://tigges.es/portfolio/casa-mirasol-neu/ | CASA MIRASOL - TIGGES ARCHITEKT | Casa Mirasol \| TIGGES ARCHITEKT | Casa Mirasol at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Casa Mirasol | DRAFT (rule-based) |
| https://tigges.es/portfolio/extension-of-residence-2/ | EXTENSION OF RESIDENCE - TIGGES ARCHITEKT | Extension Of Residence \| TIGGES ARCHITEKT | Extension Of Residence at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Extension Of Residence | DRAFT (rule-based) |
| https://tigges.es/portfolio/historic-building-gets-passivhouse/ | NAVARRA BUILDING FORUM - TIGGES ARCHITEKT | Navarra Building Forum \| TIGGES ARCHITEKT | Navarra Building Forum at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Navarra Building Forum | DRAFT (rule-based) |
| https://tigges.es/portfolio/can-titella-neu/ | CAN TITELLA - TIGGES ARCHITEKT | Can Titella \| TIGGES ARCHITEKT | Can Titella at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Can Titella | DRAFT (rule-based) |
| https://tigges.es/portfolio/historic-building-gets-efficient-passivhaus/ | THREE MOUNTAIN HOUSES - TIGGES ARCHITEKT | Three Mountain Houses \| TIGGES ARCHITEKT | Three Mountain Houses at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Three Mountain Houses | DRAFT (rule-based) |
| https://tigges.es/portfolio/low-tech-passive-house/ | VERNACULAR ARCHITECTURE XXI - TIGGES ARCHITEKT | Vernacular Architecture Xxi \| TIGGES ARCHITEKT | Vernacular Architecture Xxi at TIGGES ARCHITEKT in Tigges Architekt. See prices and opening hours, and book online. | Vernacular Architecture Xxi | DRAFT (rule-based) |

## 3. Steps on wordpress

- **schema-missing** (critical, ×1) — Add JSON-LD for LocalBusiness (see schema/ templates)  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **h1** (high, ×4) — Add exactly one descriptive H1 containing the primary topic  
  _How:_ Elementor Heading widget → Content → HTML Tag = H1. Make sure the theme isn't also printing the page title as an H1 (Elementor → Page settings → Hide title).
- **title-quality** (high, ×12) — Use a readable keyword title, not a design label  
  _How:_ Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **lcp** (high, ×1) — Compress/preload hero image, cut render-blocking JS  
  _How:_ Cloudways: turn on Breeze or Varnish, Object Cache Pro and the Cloudflare Enterprise add-on. Serve the hero as WebP with fetchpriority=high (Elementor → Image → optimise). Remove unused Elementor widgets (Elementor → Features → Improved asset loading).
- **title-length** (medium, ×2) — Aim for 30–60 chars: primary keyword + location/brand  
  _How:_ Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **thin-content** (medium, ×16) — Expand with useful, specific text (services, FAQs, proof)  
  _How:_ Add sections in Elementor; Yoast readability/word count helps.
- **canonical** (medium, ×1) — Self-reference unless intentional  
  _How:_ Yoast → Advanced → Canonical URL.
- **duplicate-title** (medium, ×3) — Make titles unique  
  _How:_ Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **expected-page** (medium, ×2) — Add a dedicated prices page and link it from the navigation  
  _How:_ Pages → Add New (Elementor), then add it to Appearance → Menus.
- **keyword-targeting** (medium, ×1) — Map each primary keyword to one page and use it in title + H1  
  _How:_ Set the focus keyphrase in Yoast/Rank Math, and use it in the SEO title and the Elementor heading widget (HTML tag H1).
- **schema-address** (medium, ×1) — Include address in the main entity markup  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **schema-telephone** (medium, ×1) — Include telephone in the main entity markup  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **schema-openingHoursSpecification** (medium, ×1) — Include openingHoursSpecification in the main entity markup  
  _How:_ Yoast/Rank Math → Settings → Site representation (Organisation / Local business). For a salon: Rank Math Local SEO module or the Yoast Local SEO add-on sets the LocalBusiness subtype, hours and geo. Otherwise paste JSON-LD with a code-snippets plugin (WPCode).
- **answer-content** (medium, ×1) — Add an FAQ / Q&A section answering real customer questions (visible text, not just schema)  
  _How:_ Add an FAQ section (Elementor Accordion). It's visible text for AI answers; FAQ rich results no longer show.
- **alt-text** (low, ×20) — Describe images; include service/location naturally  
  _How:_ Media Library → image → Alternative Text.
- **llms.txt** (low, ×1) — Optional: publish /llms.txt (cheap, low evidence of impact)  
  _How:_ Yoast (v25+) and Rank Math can generate llms.txt, or upload a file to the web root via SFTP (Cloudways → Application → Access details).

## 4. llms.txt summary

> TIGGES ARCHITEKT Architecture studio in Spain (Tigges family). tiggesarchitekt.ch redirects here.


# Fix pack — YUZU NEW

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — run with --llm (Gemini first, then Claude) or rewrite in a session.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://yuzu.hair/#entity",
  "name": "Yuzu Hair & Beauty",
  "url": "https://yuzu.hair/",
  "description": "Japanese-inspired hair salon in Dickens Yard, a short walk from Ealing Broadway station, offering cuts, blow-dries, colour, balayage and Brazilian blow-dry.",
  "telephone": "+442088402244",
  "email": "info@yuzuhairandbeauty.co.uk",
  "priceRange": "££",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "5 Dickens Yard, Longfield Avenue",
    "addressLocality": "Ealing",
    "addressRegion": "London",
    "postalCode": "W5 2TD",
    "addressCountry": "GB"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 51.5138,
    "longitude": -0.3068
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
      ],
      "opens": "10:00",
      "closes": "20:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Saturday"
      ],
      "opens": "09:00",
      "closes": "18:00"
    }
  ],
  "sameAs": [
    "https://www.instagram.com/yuzuhairandbeauty/",
    "https://www.facebook.com/YUZUHairandBeauty/",
    "https://www.tiktok.com/@yuzuhairandbeauty.est16"
  ],
  "potentialAction": {
    "@type": "ReserveAction",
    "target": "https://phorest.com/book/salons/yuzuhairandbeauty"
  }
}
```

## 2. Page titles, descriptions, H1

| Page | Now | Proposed title | Proposed description | H1 | Source |
|---|---|---|---|---|---|
| https://yuzu.hair/ | Yuzu Hair & Beauty \| Japanese hair salon, Ealing Broadway | Hair salon Ealing \| Yuzu Hair & Beauty | Hair salon Ealing at Yuzu Hair & Beauty. See prices and opening hours, and book online. | Hair salon Ealing | DRAFT (rule-based) |
| https://yuzu.hair/prices/ | Price list \| Yuzu Hair & Beauty, Ealing Broadway | Price List \| Yuzu Hair & Beauty | Price List at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Price List | DRAFT (rule-based) |
| https://yuzu.hair/offers/ | Exclusive offers \| Yuzu Hair & Beauty, Ealing | Exclusive Offers \| Yuzu Hair & Beauty | Exclusive Offers at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Exclusive Offers | DRAFT (rule-based) |
| https://yuzu.hair/team/ | Join our team \| Yuzu Hair & Beauty, Ealing | Join Our Team \| Yuzu Hair & Beauty | Join Our Team at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Join Our Team | DRAFT (rule-based) |
| https://yuzu.hair/questions/ | Questions \| Yuzu Hair & Beauty, Ealing | Questions \| Yuzu Hair & Beauty | Questions at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Questions | DRAFT (rule-based) |
| https://yuzu.hair/patch/ | Mandatory patch testing \| Yuzu Hair & Beauty | Mandatory Patch Testing \| Yuzu Hair & Beauty | Mandatory Patch Testing at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Mandatory Patch Testing | DRAFT (rule-based) |
| https://yuzu.hair/terms/ | Terms and conditions \| Yuzu Hair & Beauty | Terms And Conditions \| Yuzu Hair & Beauty | Terms And Conditions at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Terms And Conditions | DRAFT (rule-based) |
| https://yuzu.hair/privacy/ | Privacy \| Yuzu Hair & Beauty | Privacy \| Yuzu Hair & Beauty | Privacy at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Privacy | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/team.html | Join our team \| Yuzu Hair & Beauty, Ealing | Join Our Team \| Yuzu Hair & Beauty | Join Our Team at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Join Our Team | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/prices.html | Price list \| Yuzu Hair & Beauty, Ealing Broadway | Price List \| Yuzu Hair & Beauty | Price List at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Price List | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/offers.html | Exclusive offers \| Yuzu Hair & Beauty, Ealing | Exclusive Offers \| Yuzu Hair & Beauty | Exclusive Offers at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Exclusive Offers | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/contact.html | Contact \| Yuzu Hair & Beauty, Ealing | Send A Message \| Yuzu Hair & Beauty | Send A Message at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Send A Message | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/about.html | About \| Yuzu Hair & Beauty, Ealing | About \| Yuzu Hair & Beauty | About at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | About | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/questions.html | Questions \| Yuzu Hair & Beauty, Ealing | Questions \| Yuzu Hair & Beauty | Questions at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Questions | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/patch.html | Mandatory patch testing \| Yuzu Hair & Beauty | Mandatory Patch Testing \| Yuzu Hair & Beauty | Mandatory Patch Testing at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Mandatory Patch Testing | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/terms.html | Terms and conditions \| Yuzu Hair & Beauty | Terms And Conditions \| Yuzu Hair & Beauty | Terms And Conditions at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Terms And Conditions | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/privacy.html | Privacy \| Yuzu Hair & Beauty | Privacy \| Yuzu Hair & Beauty | Privacy at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Privacy | DRAFT (rule-based) |
| https://yuzu.hair/wp-content/themes/yuzu-round/static/index.html | Yuzu Hair & Beauty \| Japanese hair salon, Ealing Broadway | Where Tradition Meets Trend \| Yuzu Hair & Beauty | Where Tradition Meets Trend at Yuzu Hair & Beauty in Ealing. See prices and opening hours, and book online. | Where Tradition Meets Trend | DRAFT (rule-based) |

## 3. Steps on wordpress

- **legacy-site: https://www.yuzuhairandbeauty.london/** (high, ×1) — 301-redirect the whole domain to the main site. old Wix site — once yuzu.hair is final, 301 it (page by page) to the matching yuzu.hair URL and keep the domain  
  _How:_ At the domain host (e.g. One.com / GoDaddy): add a permanent 301 forward of the whole domain to the main site.
- **legacy-site: https://yuzuhairandbeauty.ueniweb.com/** (high, ×1) — Take it offline (delete the site or the listing on that platform). old ueni site: says West Ealing, 22 Mattock Lane W5 5BH, 07572 107373  
  _How:_ ueni: log in at ueni.com → Settings → Delete website (or ask ueni support), then request removal in Google Search Console → Removals if it still shows.
- **legacy-site: https://yuzuhairandbeauty.co.uk/** (high, ×1) — 301-redirect the whole domain to the main site. email domain shows a One.com 'under construction' page — 301 it to yuzu.hair  
  _How:_ At the domain host (e.g. One.com / GoDaddy): add a permanent 301 forward of the whole domain to the main site.
- **canonical** (medium, ×17) — Self-reference unless intentional  
  _How:_ Yoast → Advanced → Canonical URL.
- **thin-content** (medium, ×10) — Expand with useful, specific text (services, FAQs, proof)  
  _How:_ Add sections in Elementor; Yoast readability/word count helps.
- **duplicate-title** (medium, ×8) — Make titles unique  
  _How:_ Edit page → Yoast SEO (or Rank Math) panel → SEO title. Site-wide templates are under Yoast → Settings → Content types.
- **keyword-targeting** (medium, ×3) — Map each primary keyword to one page and use it in title + H1  
  _How:_ Set the focus keyphrase in Yoast/Rank Math, and use it in the SEO title and the Elementor heading widget (HTML tag H1).
- **alt-text** (low, ×2) — Describe images; include service/location naturally  
  _How:_ Media Library → image → Alternative Text.
- **email-domain** (low, ×1) — Use an address on the site domain, or redirect the old domain to the site
- **profile-link** (low, ×1) — Link profiles and add them to schema sameAs
- **llms.txt** (low, ×1) — Optional: publish /llms.txt (cheap, low evidence of impact)  
  _How:_ Yoast (v25+) and Rank Math can generate llms.txt, or upload a file to the web root via SFTP (Cloudways → Application → Access details).

## 4. llms.txt summary

> Yuzu Hair & Beauty Japanese-inspired hair salon in Dickens Yard, a short walk from Ealing Broadway station, offering cuts, blow-dries, colour, balayage and Brazilian blow-dry. Address: 5 Dickens Yard, Longfield Avenue, Ealing, London W5 2TD. Hours: Tue, Wed, Thu, Fri 10:00–20:00; Sat 09:00–18:00. Phone 020 8840 2244. Book online: https://phorest.com/book/salons/yuzuhairandbeauty

## 5. Q&A block (visible on the page; answers to be written from real facts)

**How much is a haircut at Yuzu in Ealing?**  
_Answer: …_
**Do I need a patch test before hair colour?**  
_Answer: …_
**Which hair salons in Ealing are near the station?**  
_Answer: …_

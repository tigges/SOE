# Fix pack — Yuzu Hair & Beauty (Sept 26)

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — run with --llm (Gemini first, then Claude) or rewrite in a session.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://tigges.github.io/YUZU_SEPT_26/?v=clean/#entity",
  "name": "Yuzu Hair & Beauty",
  "url": "https://tigges.github.io/YUZU_SEPT_26/?v=clean/",
  "description": "Sept 2026 rebuild (Clean variant) of the Japanese-inspired hair salon in Dickens Yard, Ealing Broadway: cuts, colour, balayage and Brazilian blow-dry.",
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
| https://tigges.github.io/YUZU_SEPT_26/ | Yuzu Hair & Beauty · Ealing Broadway | Hair Salon Ealing \| Yuzu Hair & Beauty Dickens Yard | Japanese-inspired hair salon in Ealing Broadway. Cuts, colour, balayage & Brazilian blow-dry at Dickens Yard, W5 2TD. Book online or call 020 8840 2244. | Hair Salon Ealing Broadway – Yuzu Hair & Beauty | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/hairdresser-ealing-broadway |  | Hairdresser Ealing Broadway \| Yuzu Dickens Yard W5 | Expert hairdressers at Yuzu in Ealing Broadway. Located in Dickens Yard near the station. Open Tuesday-Saturday. Book your appointment online today. | Hairdresser Ealing Broadway at Dickens Yard | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/japanese-hair-salon-london |  | Japanese Hair Salon London \| Yuzu Ealing Broadway | Experience Japanese-inspired hair care at Yuzu in Ealing, London. Traditional techniques with modern styling at Dickens Yard. Book your visit now. | Japanese Hair Salon in London – Yuzu Ealing | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/services |  | Hair Services Ealing \| Balayage, Colour & Blow Dry | Hair services at Yuzu Ealing: balayage, colour, Brazilian blow-dry, cuts and Japanese head spa. View our treatments and book online at Dickens Yard. | Hair Services at Yuzu Ealing Broadway | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/prices |  | Hair Salon Prices \| Yuzu Ealing Broadway W5 2TD | Transparent pricing for cuts, colour, balayage and treatments at Yuzu Hair & Beauty in Ealing. View our price menu or call 020 8840 2244 for details. | Prices at Yuzu Hair & Beauty Ealing | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/contact |  | Contact Yuzu Hair Salon \| Ealing Broadway W5 2TD | Visit Yuzu at 5 Dickens Yard, Longfield Avenue, Ealing W5 2TD. Call 020 8840 2244 or email info@yuzuhairandbeauty.co.uk. Near Ealing Broadway station. | Contact Yuzu Hair & Beauty Ealing | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/about |  | About Yuzu Hair & Beauty \| Japanese Salon Ealing | Meet the team at Yuzu Hair & Beauty in Ealing Broadway. Japanese-inspired salon at Dickens Yard since 2016. Learn about our stylists and approach. | About Yuzu Hair & Beauty | Claude draft |

## 3. Steps on other

- **schema-missing** (critical, ×1) — Add JSON-LD for LocalBusiness (see schema/ templates)
- **host-canonicalisation** (high, ×2) — 301 all variants to https://tigges.github.io/YUZU_SEPT_26/
- **sitemap** (high, ×1) — Generate an XML sitemap and submit it in GSC/Bing
- **h1** (high, ×1) — Add exactly one descriptive H1 containing the primary topic
- **js-only-links** (high, ×1) — Render navigation and key content server-side so crawlers and AI bots can follow links
- **nap-phone** (high, ×1) — Show the phone in the footer on every page
- **nap-postcode** (high, ×1) — Show the full address in the footer
- **extractable-text** (high, ×1) — AI answers quote text: add concise factual paragraphs (who/what/where/price/hours)
- **lcp** (high, ×1) — Compress/preload hero image, cut render-blocking JS
- **robots.txt** (medium, ×1) — Publish robots.txt with Sitemap: line
- **thin-content** (medium, ×1) — Expand with useful, specific text (services, FAQs, proof)
- **expected-page** (medium, ×4) — Add a dedicated prices page and link it from the navigation
- **keyword-targeting** (medium, ×3) — Map each primary keyword to one page and use it in title + H1
- **answer-content** (medium, ×1) — Add an FAQ / Q&A section answering real customer questions (visible text, not just schema)
- **og-image** (low, ×1) — Set a share image (1200×630)
- **email-domain** (low, ×1) — Use an address on the site domain, or redirect the old domain to the site
- **profile-link** (low, ×4) — Link profiles and add them to schema sameAs
- **llms.txt** (low, ×1) — Optional: publish /llms.txt (cheap, low evidence of impact)

## 4. llms.txt summary

> Yuzu Hair & Beauty Sept 2026 rebuild (Clean variant) of the Japanese-inspired hair salon in Dickens Yard, Ealing Broadway: cuts, colour, balayage and Brazilian blow-dry. Address: 5 Dickens Yard, Longfield Avenue, Ealing, London W5 2TD. Hours: Tue, Wed, Thu, Fri 10:00–20:00; Sat 09:00–18:00. Phone 020 8840 2244. Book online: https://phorest.com/book/salons/yuzuhairandbeauty

## 5. Q&A block (visible on the page; answers to be written from real facts)

**How much is a haircut at Yuzu in Ealing?**  
_Answer: …_
**Do I need a patch test before hair colour?**  
_Answer: …_
**Which hair salons in Ealing are near the station?**  
_Answer: …_

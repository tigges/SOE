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
| https://tigges.github.io/YUZU_SEPT_26/ | Hair Salon Ealing Broadway \| Yuzu Hair & Beauty | Hair Salon Ealing Broadway \| Yuzu Hair & Beauty | Japanese-inspired hair salon in Dickens Yard, 2 min from Ealing Broadway station. Cuts, colour, balayage & Brazilian blow-dry. Book online today. | Hair salon Ealing: Japanese-inspired cuts & colour | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/services.html | Hair Salon Services in Ealing \| Yuzu Hair | Balayage Ealing \| Yuzu Hair & Beauty Services | Balayage, hair colour, Brazilian blow-dry and cuts at Yuzu Hair & Beauty, Dickens Yard, Ealing Broadway. View services and book your appointment online. | Balayage Ealing: colour, cuts & treatments at Yuzu | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/prices.html | Hair Price List Ealing Broadway \| Yuzu Hair | Brazilian Blow Dry Ealing Prices \| Yuzu Hair | Brazilian blow-dry, balayage, colour and cut prices at Yuzu Hair & Beauty in Ealing. Senior and stylist menus available. Call 020 8840 2244 to book. | Brazilian blow dry Ealing: prices at Yuzu Hair | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/contact.html | Contact the Hairdresser Ealing Broadway | Hairdresser Ealing Broadway \| Contact Yuzu Hair | Find Yuzu Hair & Beauty at 5 Dickens Yard, Longfield Avenue, Ealing W5 2TD. Phone 020 8840 2244. Hours Tue–Fri 10–8, Sat 9–6. Book your appointment now. | Hairdresser Ealing Broadway: contact Yuzu Hair | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/about.html | About the Team at Yuzu Hair Ealing | Japanese Hair Salon London \| About Yuzu Ealing | Meet the stylists at Yuzu Hair & Beauty, a Japanese hair salon in Dickens Yard, Ealing Broadway. Expert cuts, colour and Brazilian blow-dry treatments. | Japanese hair salon London: meet the Yuzu team | Claude draft |
| https://tigges.github.io/YUZU_SEPT_26/questions.html | Questions at the Hair Salon in Ealing | Hair Colour Ealing FAQs \| Yuzu Hair & Beauty | Hair colour patch tests, haircut prices, opening hours and directions to Yuzu Hair & Beauty next to Ealing Broadway station. Get answers and book today. | Hair colour Ealing: your questions answered | Claude draft |

## 3. Steps on other

- **host-canonicalisation** (high, ×2) — 301 all variants to https://tigges.github.io/YUZU_SEPT_26/
- **content-in-pdf** (medium, ×1) — Publish that content as HTML (crawlable, quotable by AI); keep PDF as a download
- **lcp** (medium, ×1) — Compress/preload hero image, cut render-blocking JS
- **email-domain** (low, ×1) — Use an address on the site domain, or redirect the old domain to the site

## 4. llms.txt summary

> Yuzu Hair & Beauty Sept 2026 rebuild (Clean variant) of the Japanese-inspired hair salon in Dickens Yard, Ealing Broadway: cuts, colour, balayage and Brazilian blow-dry. Address: 5 Dickens Yard, Longfield Avenue, Ealing, London W5 2TD. Hours: Tue, Wed, Thu, Fri 10:00–20:00; Sat 09:00–18:00. Phone 020 8840 2244. Book online: https://phorest.com/book/salons/yuzuhairandbeauty

## 5. Q&A block (visible on the page; answers to be written from real facts)

**How much is a haircut at Yuzu in Ealing?**  
_Answer: …_
**Do I need a patch test before hair colour?**  
_Answer: …_
**Which hair salons in Ealing are near the station?**  
_Answer: …_

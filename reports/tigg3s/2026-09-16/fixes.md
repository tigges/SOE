# Fix pack — TIGGES

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — run with --llm (Gemini first, then Claude) or rewrite in a session.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://tigg3s.com/#entity",
  "name": "TIGGES",
  "url": "https://tigg3s.com/",
  "description": "TIGGES is the Tigges family and ventures hub: Art Leon, Art Barbara, architecture in Spain, DJ URBANT, Set Radar, and GTA VI.AI.",
  "sameAs": [
    "https://www.instagram.com/_urbant_/?hl=en",
    "https://www.mixcloud.com/urbant/",
    "https://www.youtube.com/@DJ_UrbanT",
    "https://twitter.com/DJUrbanT",
    "https://www.twitch.tv/djurbant",
    "https://www.linkedin.com/in/tigges/"
  ]
}
```

## 2. Page titles, descriptions, H1

| Page | Now | Proposed title | Proposed description | H1 | Source |
|---|---|---|---|---|---|
| https://tigg3s.com/ | TIGGES — Family and ventures hub | TIGGES \| TIGGES | TIGGES at TIGGES. Listen, see upcoming dates and get in touch for bookings. | TIGGES | DRAFT (rule-based) |
| https://tigg3s.com/about.html | About TIGGES — Family and ventures | About Tigges \| TIGGES | About Tigges at TIGGES. Listen, see upcoming dates and get in touch for bookings. | About Tigges | DRAFT (rule-based) |

## 3. Steps on other

- **host-canonicalisation** (high, ×2) — 301 all variants to https://tigg3s.com/
- **extractable-text** (high, ×1) — AI answers quote text: add concise factual paragraphs (who/what/where/price/hours)
- **thin-content** (medium, ×2) — Expand with useful, specific text (services, FAQs, proof)
- **expected-page** (medium, ×1) — Add a dedicated contact/booking page and link it from the navigation
- **keyword-targeting** (medium, ×2) — Map each primary keyword to one page and use it in title + H1
- **lcp** (medium, ×1) — Compress/preload hero image, cut render-blocking JS
- **alt-text** (low, ×1) — Describe images; include service/location naturally

## 4. llms.txt summary

> TIGGES TIGGES is the Tigges family and ventures hub: Art Leon, Art Barbara, architecture in Spain, DJ URBANT, Set Radar, and GTA VI.AI.

## 5. Q&A block (visible on the page; answers to be written from real facts)

**What is TIGGES?**  
_Answer: …_
**Who is DJ URBANT?**  
_Answer: …_
**Where is the Tigges architecture studio?**  
_Answer: …_

# Yuzu Hair & Beauty — SOE action plan (baseline 15 Sep 2026)

**Site:** https://www.yuzuhairandbeauty.london
**Current setup:** Wix site, Phorest booking. The WordPress rebuild is still planned.
**Baseline SOE score:** 72/100 (v2 audit, 15 Sep 2026). Full audit: `reports/yuzu/2026-09-15/report.md`. Page copy: `projects/yuzu/copy.yaml`. Fix pack: `reports/yuzu/2026-09-15/fixes.md`.

| Layer | Score | Main issue |
|---|---|---|
| Technical | 100 | Fine: HTTPS, www/apex redirects, sitemap and robots.txt all work |
| On-page | **3** | No meta descriptions anywhere; no H1 on the homepage; titles like "H O M E"; no Ealing keywords; **Wix placeholder text on the three job pages**; no services page |
| Structured data | 76 | Only `WebSite` markup, no `HairSalon` / LocalBusiness |
| Entity (name/address/phone) | 92 on-site | Brand name varies (Yuzu Hair / YUZU Hair & Beauty); email is on the .co.uk domain |
| AI readiness | 96 | Bots allowed, llms.txt exists, **but its summary describes the T&Cs page** and never says "Ealing" |
| Performance (mobile lab, median of 3) | 79 | LCP 2.5s (borderline), TBT 693ms (a risk for INP). Lighthouse SEO scored 85 |

**Against competitors** (same audit, speed excluded): Yuzu 71 is last. Therapy@Visage 89, Blo Bar 85 (also in Dickens Yard), M&M 84, CMF 81, Bella & Bello 80. Most of the gap is on-page; Therapy@Visage and Blo Bar already have LocalBusiness markup.

**Off-site** (`soe_citations.py`):
- Make It Ealing and beautynailhairsalons match.
- The **old ueniweb site shows the wrong address and phone** (22 Mattock Lane, W5 5BH, 07572 107373). Take it down.
- Old Facebook posts show 26 High Street, W5 5DB.
- Facebook, Instagram, TikTok, LinkedIn, Wheree and Phorest block automated reading, so they need checking by hand.
- No known listing on 17 directories, including Google Business Profile (add its URL), Bing, Apple, Yell, Treatwell, Fresha and Booksy.

**AI answers:** 12 checks (3 prompts × 4 engines) are waiting in `data/yuzu/ai_log.csv`.

---

## Week 1: quick wins in the Wix editor (about 2 hours)

### 1. Page SEO (Wix → page → SEO basics)

| Page | New title | Meta description |
|---|---|---|
| Home | Japanese Hair Salon in Ealing Broadway \| Yuzu Hair & Beauty | Japanese-inspired hair salon in Dickens Yard, 2 min from Ealing Broadway station. Cuts, colour, balayage & Brazilian blow-dry. Book online. |
| Offers (rename the slug `/o-f-f-e-r-s-1` → `/offers` and add a 301 redirect) | Salon Offers in Ealing — Colour & Blow-Dry Deals \| Yuzu | Weekday colour discounts, Brazilian blow-dry Wednesdays, refer-a-friend credit and 10% off when you rebook. See this month's Yuzu offers. |
| Terms | Salon Terms, Patch Tests & Cancellation Policy \| Yuzu Hair | Patch-test requirements, 48-hour cancellation policy and our two-week redo promise at Yuzu Hair & Beauty, Ealing W5. |
| Join the team (`/items`; rename to `/careers`) | Hairdresser Jobs in Ealing — Join Yuzu Hair & Beauty | Senior stylist, stylist and model vacancies at a Japanese-inspired salon in Ealing Broadway. Apply today. |

### 2. Homepage headings

- Change the "H A I R" heading to an H1 that reads **"Japanese-inspired hair salon in Ealing Broadway"**. Keep the spaced letters as styling only (CSS letter-spacing), not as the actual text.
- Keep the other headings (Price list, Offers, Contact) as H2s.

### 3. Structured data (Wix → Home → SEO → Advanced → Structured data → Add new)

- Paste the JSON-LD below.
- Check it with the Rich Results Test.

### 4. llms.txt (Wix SEO settings)

Replace the summary with:

> Yuzu Hair & Beauty is a Japanese-inspired hair salon at 5 Dickens Yard, Longfield Avenue, Ealing, London W5 2TD, a short walk from Ealing Broadway station. Services: cuts, blow-dries, colour, balayage, Brazilian blow-dry. Open Tue–Fri 10:00–20:00, Sat 09:00–18:00. Book online via Phorest or call 020 8840 2244.

### 5. Job pages

Replace the Wix placeholder text ("This is placeholder text…") on Senior Stylists, Stylists and Models: Content Manager → the jobs collection. New titles and descriptions for these pages are in `copy.yaml`.

### 6. Images

- Add alt text to the 2 images that don't have it.
- Set a social share image (1200×630) for every page.

## Weeks 2–4: content and entity

6. **Price list as HTML.** Turn the PDF price list into a `/prices` page and keep the PDF as a download. Prices are the facts AI answers quote most.
7. **Service pages.** Create four pages, one per main service keyword: `/balayage-ealing`, `/brazilian-blow-dry-ealing`, `/hair-colour-ealing`, `/haircuts-ealing`. Each needs 300+ words, the price, the stylists who do it, before/after photos and a Q&A block.
8. **Team page.** Add real stylist bios: experience, specialisms, Japanese techniques. These are experience and expertise signals.
9. **One name everywhere.** Use "Yuzu Hair & Beauty" on the site, Google Business Profile, Instagram, Facebook and Phorest. Also consider moving email to @yuzuhairandbeauty.london, or at least 301-redirect yuzuhairandbeauty.co.uk to the site.
10. **Clean up old listings.** Remove or update the old "26 High Street W5 5DB" references on Facebook, the old ueniweb site (West Ealing) and the unclaimed Wheree listing.

## Months 2–3: authority and local

11. **Google Business Profile.**
    - Primary category: *Hair salon*. Add *Beauty salon* only if Yuzu offers those services.
    - Add every service with its price, weekly posts, 10+ new photos and a short video each month, and a Phorest booking link.
    - Reply to every review.
12. **Review engine.** After each visit, Phorest sends an automatic review request by SMS or email linking to Google. Aim for 15–25 new reviews a month.
13. **Listings and mentions.**
    - Bing Places (import from Google Business Profile) and Apple Business Connect.
    - Yell, Thomson Local, Cylex, FreeIndex, Yelp UK, Nextdoor.
    - Make It Ealing (claim or update the listing).
    - Treatwell and/or Fresha. These rank on page 1 for "hair salon Ealing" and are often cited by AI answers.
14. **Local PR.** Pitch Ealing Times, Dickens Yard / St George, and "best Japanese head spa London" roundups.

## Performance (only if it stays on Wix)

- Remove unused Wix apps and widgets.
- Compress the hero image to under 200 KB (WebP).
- Avoid autoplaying video or galleries above the fold.
- Target: mobile LCP ≤ 2.5s.

## Tracking

- Run the audit monthly (GitHub Action).
- Search Console: impressions for "salon Ealing" terms.
- Business Profile: calls, direction requests, bookings.
- AI prompt log: the 3 prompts in `configs/yuzu.yaml`, run in ChatGPT, Perplexity, Gemini and Google AI Mode. Record whether Yuzu is mentioned or cited, and which sources are cited instead.

---

## JSON-LD to paste (HairSalon)

Coordinates are from postcodes.io (the postcode centroid). Check the exact entrance on Google Maps.

```json
{
  "@context": "https://schema.org",
  "@type": "HairSalon",
  "@id": "https://www.yuzuhairandbeauty.london/#business",
  "name": "Yuzu Hair & Beauty",
  "url": "https://www.yuzuhairandbeauty.london/",
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
  "geo": { "@type": "GeoCoordinates", "latitude": 51.5138, "longitude": -0.3068 },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday","Friday"], "opens": "10:00", "closes": "20:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "18:00" }
  ],
  "sameAs": [
    "https://www.instagram.com/yuzuhairandbeauty/",
    "https://www.facebook.com/YUZUHairandBeauty/"
  ],
  "potentialAction": {
    "@type": "ReserveAction",
    "target": "https://phorest.com/book/salons/yuzuhairandbeauty"
  }
}
```

Before publishing, add `logo` and `image` URLs from the Wix media library, and a `hasMap` link to the Google Business Profile.

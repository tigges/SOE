# Yuzu Hair & Beauty — SOE action plan (baseline 15 Sep 2026)

**Site:** https://www.yuzuhairandbeauty.london
**Current setup:** Wix site, Phorest booking. The WordPress rebuild is still planned.
**Baseline SOE score:** 65/100 (v2 audit, stricter scoring, 15 Sep 2026). Full audit: `reports/yuzu/2026-09-15/report.md`. Page copy: `projects/yuzu/copy.yaml`. Fix pack: `reports/yuzu/2026-09-15/fixes.md`.

| Layer | Score | Main issue |
|---|---|---|
| Technical | 100 | Fine: HTTPS, www/apex redirects, sitemap and robots.txt all work |
| On-page | **3** | No meta descriptions anywhere; no H1 on the homepage; titles like "H O M E"; no Ealing keywords; **Wix placeholder text on the three job pages**; no services page |
| Structured data | **40** (capped: no entity markup) | Only `WebSite` markup, no `HairSalon` / LocalBusiness |
| Entity (name/address/phone) | 92 on-site | Brand name varies (Yuzu Hair / YUZU Hair & Beauty); email is on the .co.uk domain |
| AI readiness | 96 | Bots allowed, llms.txt exists, **but its summary describes the T&Cs page** and never says "Ealing" |
| Performance (mobile lab, median of 3) | 69 | LCP 3.3s, TBT 956ms (a risk for INP). Lighthouse SEO scored 85 |

**Against competitors** (same audit, speed excluded): Yuzu 64 is last. Therapy@Visage 89, Blo Bar 85 (also in Dickens Yard), M&M 77, Bella & Bello 75, CMF 73. Most of the gap is on-page and structured data; Therapy@Visage and Blo Bar already have LocalBusiness markup.

**Against best-in-class leaders** (`soe_benchmark.py`; speed excluded): Hershesons 87, Headmasters 83 and Ruffians 82, vs Yuzu 67. The biggest gaps are on-page (10 vs 88) and structured data (40 vs 96). All three leaders do these things that Yuzu doesn't:
- meta descriptions on every page
- 300+ words per page
- a newsletter sign-up
- rich internal linking
- lazy-loaded images
- separate content sitemaps

Two of the three also use breadcrumb and Organization markup, link to TikTok/YouTube, publish `llms-full.txt`, and structure pages with H2 sections. Hershesons shows prices as page text and uses video on every page.

**Off-site** (`soe_citations.py`, last manual check **16 Sep 2026**):
- Make It Ealing matches name, phone and postcode.
- **beautynailhairsalons.com is ignored.** It is a Singapore-operated aggregator and is disconnected from Yuzu Hair London. Do not treat it as a UK listing to maintain.
- **Wheree** (unclaimed): NAP matches 5 Dickens Yard, Longfield Ave, W5 2TD. Hours on the page only show 10:00–20:00 (not Saturday 09:00–18:00). Claim the listing.
- **Instagram** and **TikTok** bios match Unit 5, Dickens Yard, Ealing, W5 2TD. Instagram already has www.yuzuhairandbeauty.london; add that URL to the TikTok bio. Instagram hours match (Tue–Fri 10–8, Sat 9–6, Sun–Mon closed).
- **Phorest** public page (`phorest.com/salon/yuzuhairandbeauty`) matches NAP, phone and email.
- **Facebook** (logged-out): page is YUZU Hair & Beauty, Hair salon. Address is not visible; older posts still say 26 High Street, W5 5DB — update About/address.
- **LinkedIn:** company name is YUZU HAIR LIMITED; website and phone match; no street address.
- **Take the old ueni site offline:** yuzuhairandbeauty.ueniweb.com still shows "West Ealing", 22 Mattock Lane, W5 5BH and 07572 107373. Delete it in the ueni account (or ask ueni support), then request removal in Search Console → Removals.
- **Redirect yuzuhairandbeauty.co.uk:** the email domain shows a One.com "under construction" page. Set a permanent (301) forward of the whole domain to www.yuzuhairandbeauty.london, keeping the email working.
- Facebook, Instagram, TikTok, LinkedIn, Wheree and Phorest block automated reading, so they need checking by hand.
- **Remembered listing actions** (create/claim each one and set the website to https://www.yuzuhairandbeauty.london): Google Business Profile, Bing Places, Apple Business Connect, Yell, Treatwell, Fresha. These are `action: list` rows in `configs/yuzu.yaml` so they stay on the Control Room listings table until a live URL replaces them. Other directory gaps (Thomson Local, Scoot, Cylex, FreeIndex, Yelp UK, Nextdoor, Booksy, …) still show as “no known listing”.

**Same-name business:** YUZUHAIR in Hucknall, Nottingham (yuzuhair.co.uk, listed on Yell as "Yuzu Hair") competes for "Yuzu Hair" searches. It isn't a local competitor. Use "Yuzu Hair & Beauty, Ealing" consistently, and watch the AI log's new brand prompt ("Yuzu Hair salon") for answers that mix the two up.

**AI answers:** Claude and Gemini auto-checks plus a monthly Google AI Mode check. Prompts are in `configs/yuzu.yaml`.

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

11. **Google Business Profile** (remembered action — `citations:` row `action: list`).
    - Create or claim the profile. Set the website to **https://www.yuzuhairandbeauty.london**.
    - Primary category: *Hair salon*. Add *Beauty salon* only if Yuzu offers those services.
    - Add every service with its price, weekly posts, 10+ new photos and a short video each month, and a Phorest booking link.
    - Reply to every review.
    - Once live, put the Maps/GBP URL in `business.profiles.google_business` and replace the citations row URL (drop `action: list`).
12. **Review engine.** After each visit, Phorest sends an automatic review request by SMS or email linking to Google. Aim for 15–25 new reviews a month.
13. **Listings and mentions** (same remembered actions in `configs/yuzu.yaml`; website on every listing = https://www.yuzuhairandbeauty.london).
    - Bing Places (import from Google Business Profile) and Apple Business Connect.
    - Yell (the Hucknall “Yuzu Hair” Yell page is a different business). Thomson Local, Cylex, FreeIndex, Yelp UK, Nextdoor.
    - Make It Ealing (already matches — claim or update if needed).
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
- AI prompt log: the prompts in `configs/yuzu.yaml`. Claude and Gemini fill in on each SOE run; check Google AI Mode by hand. Record whether Yuzu is mentioned or cited, and which sources are cited instead.

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

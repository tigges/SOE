# Fix pack — Yuzu Hair & Beauty

Everything here is a proposal: review before publishing. Page copy marked DRAFT is rule-based — have Claude rewrite it (the /soe skill does this) or run with --llm.

## 1. Entity structured data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://www.yuzuhairandbeauty.london/#entity",
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
| https://www.yuzuhairandbeauty.london/ | H O M E \| Yuzu Hair | Japanese Hair Salon in Ealing Broadway \| Yuzu Hair & Beauty | Japanese-inspired hair salon in Dickens Yard, 2 min from Ealing Broadway station. Cuts, colour, balayage & Brazilian blow-dry. Book online today. | Japanese-inspired hair salon in Ealing Broadway | Claude draft |
| https://www.yuzuhairandbeauty.london/items/senior-stylists | Senior Stylists \| Yuzu Hair | Senior Stylist Job in Ealing Broadway \| Yuzu Hair & Beauty | Yuzu Hair & Beauty is hiring a senior stylist at our Japanese-inspired salon in Dickens Yard, Ealing W5. Read the role details and apply. | Senior stylist vacancy | Claude draft |
| https://www.yuzuhairandbeauty.london/items/stylists | Stylists \| Yuzu Hair | Hair Stylist Job in Ealing Broadway \| Yuzu Hair & Beauty | Yuzu Hair & Beauty is hiring a hair stylist at our Japanese-inspired salon in Dickens Yard, Ealing W5. Read the role details and apply. | Stylist vacancy | Claude draft |
| https://www.yuzuhairandbeauty.london/items/models | Models \| Yuzu Hair | Hair Models Wanted in Ealing \| Yuzu Hair & Beauty | Yuzu Hair & Beauty in Ealing Broadway is looking for hair models. Read what's involved and how to apply to be a model at our salon. | Hair models wanted | Claude draft |
| https://www.yuzuhairandbeauty.london/o-f-f-e-r-s-1 | OFFERS \| Yuzu Hair | Salon Offers in Ealing: Colour & Blow-Dry Deals \| Yuzu | Tuesday and Thursday colour discounts, Brazilian blow-dry Wednesdays, refer-a-friend credit and 10% off when you rebook. See this month's Yuzu offers. | Salon offers at Yuzu, Ealing | Claude draft |
| https://www.yuzuhairandbeauty.london/terms-and-conditions | TERMS AND CONDITIONS \| Yuzu Hair | Salon Terms, Patch Tests & Cancellation Policy \| Yuzu Hair | Patch-test rules for colour services, our 48-hour cancellation policy and our two-week redo promise at Yuzu Hair & Beauty, Ealing W5. | Terms, patch tests and cancellations | Claude draft |
| https://www.yuzuhairandbeauty.london/items | Items (List) \| Yuzu Hair | Hairdresser Jobs in Ealing: Join Yuzu Hair & Beauty | Senior stylist, stylist and model vacancies at a Japanese-inspired salon in Dickens Yard, Ealing Broadway. See the roles and apply today. | Join the Yuzu team | Claude draft |

## 3. Steps on wix

- **schema-missing** (critical, ×1) — Add JSON-LD for LocalBusiness (see schema/ templates)  
  _How:_ Pages & Menu → page ⋯ → SEO → Advanced SEO → Structured data markup → Add new markup. Paste JSON-LD (max 7,000 chars, up to 5 per page) and check it in the Rich Results Test.
- **title-quality** (high, ×1) — Use a readable keyword title, not a design label  
  _How:_ Editor → Pages & Menu → page ⋯ → SEO basics → Title tag. For many pages at once: Dashboard → Marketing & SEO → SEO → SEO Settings → page type → edit the title pattern.
- **meta-description** (high, ×7) — Write a 140–160 char description with a call to action  
  _How:_ Pages & Menu → page ⋯ → SEO basics → Meta description. The SEO Settings page-type pattern is the fallback.
- **h1** (high, ×3) — Add exactly one descriptive H1 containing the primary topic  
  _How:_ Select the main heading → Edit text → Semantic tag = Heading 1 (H1). Use only one per page. For spaced lettering, use letter spacing, not spaces typed between letters.
- **placeholder-text** (high, ×3) — Replace builder placeholder copy with real content (it looks unfinished to people and engines)  
  _How:_ Open the page (or the CMS collection item in Content Manager) and replace the default Wix text. Check dynamic item pages too.
- **legacy-site: https://yuzuhairandbeauty.ueniweb.com/** (high, ×1) — Take it offline (delete the site or the listing on that platform). old ueni site: says West Ealing, 22 Mattock Lane W5 5BH, 07572 107373  
  _How:_ ueni: log in at ueni.com → Settings → Delete website (or ask ueni support), then request removal in Google Search Console → Removals if it still shows.
- **legacy-site: https://yuzuhairandbeauty.co.uk/** (high, ×1) — 301-redirect the whole domain to the main site. email domain shows a One.com 'under construction' page — 301 it to the .london site  
  _How:_ At the domain host (e.g. One.com / GoDaddy): add a permanent 301 forward of the whole domain to the main site.
- **title-length** (medium, ×5) — Aim for 30–60 chars: primary keyword + location/brand  
  _How:_ Editor → Pages & Menu → page ⋯ → SEO basics → Title tag. For many pages at once: Dashboard → Marketing & SEO → SEO → SEO Settings → page type → edit the title pattern.
- **thin-content** (medium, ×5) — Expand with useful, specific text (services, FAQs, proof)  
  _How:_ Add text sections in the Editor (a Text + Image strip). Wix gives no word count, so re-run the audit afterwards.
- **content-in-pdf** (medium, ×1) — Publish that content as HTML (crawlable, quotable by AI); keep PDF as a download  
  _How:_ Rebuild the PDF content as a Wix page (or use Wix Bookings service/price lists). Keep the PDF as a download link.
- **expected-page** (medium, ×1) — Add a dedicated services page and link it from the navigation  
  _How:_ Pages & Menu → + Add page. Also add it to the menu so it's linked.
- **keyword-targeting** (medium, ×3) — Map each primary keyword to one page and use it in title + H1  
  _How:_ Put the keyword in the title tag (SEO basics) and in the page's main heading. In the Editor, select the heading text → Text settings → Semantic tag = H1.
- **schema-openingHoursSpecification** (medium, ×1) — Include openingHoursSpecification in the main entity markup  
  _How:_ Pages & Menu → page ⋯ → SEO → Advanced SEO → Structured data markup → Add new markup. Paste JSON-LD (max 7,000 chars, up to 5 per page) and check it in the Rich Results Test.
- **schema-sameAs** (medium, ×1) — Include sameAs in the main entity markup  
  _How:_ Pages & Menu → page ⋯ → SEO → Advanced SEO → Structured data markup → Add new markup. Paste JSON-LD (max 7,000 chars, up to 5 per page) and check it in the Rich Results Test.
- **brand-name** (medium, ×1) — Use one exact business name everywhere (site, GBP, directories, schema)  
  _How:_ Settings → Business info → Business name. Then use the same name in titles, the footer and every profile.
- **llms.txt-summary** (medium, ×1) — Rewrite the llms.txt summary to describe the business, not a random page  
  _How:_ Dashboard → SEO → llms.txt → edit the summary paragraph. Once edited it no longer auto-updates.
- **lcp** (medium, ×1) — Compress/preload hero image, cut render-blocking JS  
  _How:_ Remove unused apps (Apps → Manage apps). Use a compressed hero image (Wix image settings → quality). Don't put video or slideshows above the fold.
- **tbt-inp-proxy** (medium, ×1) — Remove unused apps/widgets and third-party scripts  
  _How:_ Remove unused apps and third-party embeds; limit animations (Editor → Animations).
- **alt-text** (low, ×1) — Describe images; include service/location naturally  
  _How:_ Click the image → Settings → 'What's in the image? Tell Google' (the alt text).
- **og-image** (low, ×4) — Set a share image (1200×630)  
  _How:_ Pages & Menu → page ⋯ → Social share → upload a 1200×630 image. The site-wide default is in SEO Settings.
- **email-domain** (low, ×1) — Use an address on the site domain, or redirect the old domain to the site
- **profile-link** (low, ×1) — Link profiles and add them to schema sameAs

## 4. llms.txt summary

> Yuzu Hair & Beauty Japanese-inspired hair salon in Dickens Yard, a short walk from Ealing Broadway station, offering cuts, blow-dries, colour, balayage and Brazilian blow-dry. Address: 5 Dickens Yard, Longfield Avenue, Ealing, London W5 2TD. Hours: Tue, Wed, Thu, Fri 10:00–20:00; Sat 09:00–18:00. Phone 020 8840 2244. Book online: https://phorest.com/book/salons/yuzuhairandbeauty

## 5. Q&A block (visible on the page; answers to be written from real facts)

**How much is a haircut at Yuzu in Ealing?**  
_Answer: …_
**Do I need a patch test before hair colour?**  
_Answer: …_
**Which hair salons in Ealing are near the station?**  
_Answer: …_

# TIGGES hub — first look (16 Sep 2026)

**Site:** https://tigg3s.com (www redirects here)
**What it is:** A GitHub Pages directory for the Tigges family and ventures. It is not a shop. Each card opens a studio or project site.
**Platform:** static hub (`TIGGES — Family and ventures hub`), not WordPress. The previous SOE config had `platform: wordpress` and `url: https://www.tigg3s.com`, which produced false host-canonicalisation / Elementor fixes.

## Linked websites (now their own SOE projects)

| Hub card | URL | SOE slug | Notes |
|---|---|---|---|
| Art Leon | https://leontigges.com | `leontigges` | WordPress. “Young Art from London.” |
| Art Barbara | https://barbaratigges.com | `barbaratigges` | WordPress. “Art aus Basel.” |
| Architecture | https://tiggesarchitekt.ch → **https://tigges.es** | `tigges` | WordPress + Elementor. Hub still links the .ch host; it 301s to .es. |
| Music | https://djurbant.com | `djurbant` | Already in the Control Room. |
| Set Radar | https://www.setradar.ai | `setradar` | Timed tracklists. Apex redirects to www. |
| GTA VI.AI | https://gtavi.ai | `gtavi` | Astro publisher (“Follow the GTA$”). |

Footer social (not added as sites): Mixcloud, Instagram `@_urbant_`, YouTube `@DJ_UrbanT`, X `@DJUrbanT`, Twitch `djurbant`, LinkedIn `/in/tigges/`.

## First SOE scores (16 Sep 2026)

| Site | Score | Main gap |
|---|---|---|
| TIGGES hub | **92** | LCP; one alt; no contact page (it is a directory) |
| Art Barbara | 77 | WordPress on-page / schema |
| Art Leon | 73 | WordPress on-page / schema |
| Set Radar | 75 | SaaS expected pages (pricing/docs) |
| GTA VI.AI | 69 | Publisher schema / topic pages |
| TIGGES ARCHITEKT | 68 | Thin WordPress pages, NAP |
| DJ URBANT | (existing project) | Already in the Control Room |

- Sitemap: `/` and `/about.html` only. About page already answers “What is TIGGES?”, “Who is DJ URBANT?”, architecture Spain, Set Radar, GTA VI.AI.
- Schema on the hub: FAQPage + Organization + Person + WebSite (strong for a two-page directory).
- Main leftover issues: LCP, one missing image alt, no separate contact page (the hub is the directory).

## Suggested next steps on the hub

1. Point the architecture card at https://tigges.es (the live host), not tiggesarchitekt.ch.
2. Keep one name: **TIGGES** (not `www.tigg3s.com`).
3. Treat IndexNow as GitHub Pages (`/indexnow.txt` on the apex), not WordPress.

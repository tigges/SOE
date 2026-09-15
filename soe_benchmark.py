#!/usr/bin/env python3
"""
SOE benchmark — compare a site with best-in-class "leader" sites to find improvements
the audit doesn't score yet, and new SEO/AI-search tactics worth adopting.

Usage:
    python soe_benchmark.py configs/<slug>.yaml [--out reports/<slug>/<date>] [--pages 25]
    python soe_benchmark.py --discover <type> URL [URL ...]    # score candidate leaders, best first

Config:
    benchmarks:                 # aspirational leaders (not necessarily local rivals)
      - {name: "Hershesons", url: https://www.hershesons.com, why: "London salon group, best score of 15 tested"}

How it works
  1. Runs the same audit on this site and each leader (no Lighthouse).
  2. Builds a "virtual 100": the best score per layer across all leaders.
  3. Takes a feature inventory of every page (≈40 features: schema types, FAQ blocks, prices, reviews,
     video, maps, breadcrumbs, modern images, blog, team pages, llms.txt, AI-bot policy, sitemap types…).
  4. Reports gaps: features leaders use on many pages that this site lacks. Features the audit
     doesn't check yet are flagged "new check candidate" — that's how the template learns.
Writes benchmark.json and benchmark.md.
"""
import argparse, datetime as dt, json, os, re, sys
from urllib.parse import urlparse

import requests, yaml
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import soe_audit  # noqa: E402

LAYERS = ["Technical", "On-page", "Structured data", "Entity / NAP", "AI search readiness"]

# key: (label, idea, already scored by soe_audit?)
FEATURES = {
    "meta_description": ("Meta description", "Unique meta description on every page", True),
    "og_image": ("Share image (og:image)", "Share image on every page", True),
    "twitter_card": ("Twitter/X card", "Add twitter:card + image for richer shares", False),
    "canonical": ("Canonical tag", "Self-referencing canonical on every page", True),
    "hreflang": ("hreflang", "Language/region alternates for multi-market sites", False),
    "max_image_preview": ("Large image previews", "robots max-image-preview:large for big thumbnails in Discover/AI answers", False),
    "breadcrumbs": ("Breadcrumbs", "Visible breadcrumbs + BreadcrumbList markup", False),
    "faq_block": ("Q&A content", "Question-style headings with direct answers", True),
    "prices_html": ("Prices in HTML", "Show prices as page text (quotable by AI answers)", True),
    "reviews_onsite": ("Reviews on site", "Show real reviews/testimonials with ratings", False),
    "aggregate_rating": ("Rating markup", "AggregateRating/Review markup on pages that show reviews", False),
    "video": ("Video", "Embed short videos (YouTube/Vimeo/native) — recent video is an AI-visibility signal", False),
    "map_embed": ("Map embed", "Embed a map with the exact location on the contact page", False),
    "booking_cta": ("Booking link", "Book / buy call-to-action on every page", False),
    "tel_link": ("Click-to-call", "tel: links for mobile visitors", False),
    "team_pages": ("Team / people pages", "Individual pages for stylists/authors/artists (experience signal)", False),
    "blog": ("Articles / journal", "Regular helpful articles answering customer questions", False),
    "location_pages": ("Location / area pages", "A page per location or area served", False),
    "service_pages": ("Service pages", "One page per service with price, duration, FAQs", True),
    "gift_cards": ("Gift cards / shop", "Gift cards or products — extra landing pages and Product markup", False),
    "newsletter": ("Newsletter sign-up", "Email capture for repeat visits", False),
    "modern_images": ("WebP/AVIF images", "Serve WebP/AVIF for speed", False),
    "lazy_images": ("Lazy-loaded images", "loading=lazy below the fold", False),
    "preload": ("Preload/preconnect", "Preload hero image and fonts, preconnect to CDNs", False),
    "social_video": ("TikTok / YouTube links", "Link TikTok/YouTube profiles (and add to sameAs)", False),
    "music_links": ("Music platforms", "Link Spotify/SoundCloud/Beatport etc. (and add to sameAs)", False),
    "events": ("Events / dates", "Upcoming dates as pages with Event markup", False),
    "press": ("Press / media page", "Press kit and coverage page (mentions and links)", False),
    "rss": ("RSS feed", "RSS/Atom feed for articles", False),
    "internal_links": ("Rich internal linking", "20+ internal links per page (menus, related content)", False),
    "long_content": ("Substantial pages", "300+ words of useful text per page", True),
    "deep_headings": ("Structured headings", "3+ H2 sections per page", False),
    "site:llms_txt": ("llms.txt", "Publish /llms.txt describing the business", True),
    "site:llms_full": ("llms-full.txt", "Publish /llms-full.txt with full key content", False),
    "site:ai_policy": ("Explicit AI-bot policy", "Name AI bots (GPTBot, ClaudeBot, PerplexityBot…) in robots.txt deliberately", False),
    "site:image_sitemap": ("Image/video sitemaps", "Image or video sitemap for visual content", False),
    "site:blog_sitemap": ("Content sitemaps", "Separate sitemaps for posts/products/locations", False),
}
SCHEMA_IDEAS = {
    "FAQPage": "FAQ markup (no rich result since 2026, but machine-readable Q&A)",
    "BreadcrumbList": "Breadcrumb markup", "AggregateRating": "Rating markup", "Review": "Review markup",
    "Product": "Product markup (gift cards, retail products)", "Offer": "Offer/price markup",
    "Service": "Service markup per treatment", "Event": "Event markup for dates",
    "VideoObject": "Video markup", "Article": "Article markup", "BlogPosting": "Blog post markup",
    "Person": "Person markup for team/artist", "HairSalon": "HairSalon (LocalBusiness) markup",
    "LocalBusiness": "LocalBusiness markup", "MusicGroup": "MusicGroup markup", "ItemList": "ItemList markup",
    "SearchAction": "Sitelinks search box markup", "Organization": "Organization markup",
    "ContactPoint": "ContactPoint markup", "OpeningHoursSpecification": "Opening hours markup",
    "GeoCoordinates": "Geo coordinates markup", "HowTo": "HowTo markup (no rich result, still descriptive)",
}
UA = "Mozilla/5.0 (compatible; SOE-Audit/1.0)"


def page_features(p):
    html = p.get("raw_html", "")
    soup = BeautifulSoup(html, "lxml")
    low = html.lower()
    text = p.get("text", "")
    path = urlparse(p["url"]).path.lower()
    heads = [h.get_text(" ", strip=True) for h in soup.find_all(["h2", "h3"])]
    links = [a.get("href", "") for a in soup.find_all("a", href=True)]
    host = urlparse(p["url"]).netloc.replace("www.", "")
    internal = [l for l in links if l.startswith("/") or host in l]
    imgs = soup.find_all("img")
    f = {
        "meta_description": bool(p.get("description")),
        "og_image": bool(p.get("og_image")),
        "twitter_card": bool(soup.find("meta", attrs={"name": "twitter:card"})),
        "canonical": bool(p.get("canonical")),
        "hreflang": bool(soup.find("link", attrs={"hreflang": True})),
        "max_image_preview": "max-image-preview" in low,
        "breadcrumbs": "breadcrumb" in low,
        "faq_block": sum(h.strip().endswith("?") for h in heads) >= 2 or "faqpage" in low,
        "prices_html": len(re.findall(r"[£€$]\s?\d{2,4}", text)) >= 3,
        "reviews_onsite": bool(re.search(r"\b(testimonial|reviews?)\b", text, re.I)) and ("★" in text or "rating" in low),
        "aggregate_rating": "aggregaterating" in low or '"review"' in low,
        "video": bool(re.search(r"youtube\.com/embed|player\.vimeo|<video", low)),
        "map_embed": bool(re.search(r"google\.[a-z.]+/maps/embed|maps\.google|mapbox|openstreetmap", low)),
        "booking_cta": bool(re.search(r"\bbook( now| online| an appointment)?\b|\btickets?\b|\bshop now\b", text, re.I)),
        "tel_link": any(l.startswith("tel:") for l in links),
        "team_pages": bool(re.search(r"/(team|stylists?|people|artists?|about-us/team)(/|$)", path)),
        "blog": bool(re.search(r"/(blog|journal|news|articles?|magazine|stories)(/|$)", path)),
        "location_pages": bool(re.search(r"/(locations?|salons?|branches|find-us|stores?)(/|$)", path)),
        "service_pages": bool(re.search(r"/(services?|treatments?|menu|colour|color|cut|balayage)(/|$)", path)),
        "gift_cards": bool(re.search(r"gift[- ]?cards?|vouchers?", low)),
        "newsletter": bool(re.search(r"newsletter|subscribe", low)),
        "modern_images": bool(re.search(r"\.(webp|avif)\b|format=(webp|avif)|fm=(webp|avif)", low)),
        "lazy_images": sum(1 for i in imgs if i.get("loading") == "lazy") >= 1,
        "preload": bool(soup.find("link", rel=lambda r: r and any(x in ("preload", "preconnect") for x in r))),
        "social_video": bool(re.search(r"tiktok\.com/@|youtube\.com/(@|c/|channel/|user/)", low)),
        "music_links": bool(re.search(r"open\.spotify\.com|soundcloud\.com/|beatport\.com|music\.apple\.com|mixcloud\.com", low)),
        "events": bool(re.search(r"/(events?|tour|dates|gigs)(/|$)", path)) or '"event"' in low,
        "press": bool(re.search(r"/(press|media|epk)(/|$)", path)),
        "rss": bool(soup.find("link", attrs={"type": re.compile("rss|atom")})),
        "internal_links": len(set(internal)) >= 20,
        "long_content": p.get("words", 0) >= 300,
        "deep_headings": len(soup.find_all("h2")) >= 3,
    }
    for t in p.get("ld_types", []):
        f[f"schema:{t}"] = True
    return f


def site_features(base):
    out = {}
    get = lambda u: requests.get(u, headers={"User-Agent": UA}, timeout=20)
    try:
        r = get(base + "/llms.txt"); out["site:llms_txt"] = r.status_code == 200 and len(r.text.strip()) > 20
        r = get(base + "/llms-full.txt"); out["site:llms_full"] = r.status_code == 200 and len(r.text.strip()) > 20
        rr = get(base + "/robots.txt"); rb = rr.text if rr.status_code == 200 else ""
        out["site:ai_policy"] = bool(re.search(r"gptbot|claudebot|perplexitybot|oai-searchbot|google-extended", rb, re.I))
        sm = " ".join(re.findall(r"(?im)^sitemap:\s*(\S+)", rb)) + " "
        try:
            idx = get(base + "/sitemap.xml").text[:20000]
            sm += " ".join(re.findall(r"<loc>([^<]+)</loc>", idx)[:50])
        except requests.RequestException:
            pass
        out["site:image_sitemap"] = bool(re.search(r"image|video", sm, re.I))
        out["site:blog_sitemap"] = bool(re.search(r"post|blog|product|location|article|news", sm, re.I))
    except requests.RequestException:
        pass
    return out


def inventory(au):
    pages = list(au.pages.values())
    n = max(len(pages), 1)
    cov = {}
    for p in pages:
        for k, v in page_features(p).items():
            cov[k] = cov.get(k, 0) + (1 if v else 0)
    cov = {k: round(v / n, 2) for k, v in cov.items()}
    cov.update({k: 1.0 if v else 0.0 for k, v in site_features(au.base).items()})
    return cov


def audit_site(name, url, stype, pages, business=None):
    cfg = {"site": {"name": name, "url": url, "type": stype}, "audit": {"max_pages": pages}}
    if business:
        cfg["business"] = business
    au = soe_audit.run_audit(cfg)
    total, layers = au.score()
    return au, dict(name=name, url=url, score=total, layers=layers, pages=len(au.pages),
                    schema=au.meta.get("schema_types"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--pages", type=int, default=25)
    ap.add_argument("--discover", nargs="+", metavar=("TYPE", "URL"))
    a = ap.parse_args()

    if a.discover:
        stype, urls = a.discover[0], a.discover[1:]
        rows = []
        for u in urls:
            try:
                _, row = audit_site(u, u, stype, 12)
                rows.append(row)
            except Exception as e:
                rows.append(dict(url=u, score=0, error=str(e)[:80]))
        for r in sorted(rows, key=lambda r: -r["score"]):
            print(f"{r['score']:>3}  {r['url']}  pages={r.get('pages', 0)}  {r.get('error', '')}")
        return

    cfg = yaml.safe_load(open(a.config))
    stype = cfg["site"].get("type", "generic")
    leaders_cfg = [b for b in cfg.get("benchmarks") or [] if isinstance(b, dict) and b.get("url")]
    if not leaders_cfg:
        sys.exit("no benchmarks: in config — find candidates with --discover")
    us_au, us = audit_site(cfg["site"]["name"], cfg["site"]["url"], stype, a.pages, cfg.get("business"))
    us_inv = inventory(us_au)
    leaders, invs = [], {}
    for b in leaders_cfg:
        au, row = audit_site(b["name"], b["url"], stype, a.pages)
        row["why"] = b.get("why", "")
        leaders.append(row)
        invs[b["name"]] = inventory(au)
        print(f"  leader {b['name']}: {row['score']} ({row['pages']} pages)")

    virtual = {}
    for L in LAYERS:
        best = max(leaders, key=lambda r: r["layers"].get(L) or 0)
        virtual[L] = dict(score=best["layers"].get(L), leader=best["name"], ours=us["layers"].get(L))

    keys = set(us_inv) | {k for inv in invs.values() for k in inv}
    gaps = []
    for k in sorted(keys):
        lead = {n: inv.get(k, 0) for n, inv in invs.items()}
        best = max(lead.values())
        ours = us_inv.get(k, 0)
        if best - ours < 0.3 or best < 0.3:
            continue
        if k.startswith("schema:"):
            t = k.split(":", 1)[1]
            if t not in SCHEMA_IDEAS:
                continue
            label, idea, covered = f"{t} markup", SCHEMA_IDEAS[t], t in ("HairSalon", "LocalBusiness", "Organization", "Person", "MusicGroup")
            k_group = "Structured data"
        else:
            label, idea, covered = FEATURES.get(k, (k, k, False))
            k_group = "Site" if k.startswith("site:") else "Pages"
        adoption = sum(1 for v in lead.values() if v >= 0.3)
        gaps.append(dict(feature=k, label=label, idea=idea, group=k_group, ours=ours, leaders=lead,
                         adoption=adoption, gap=round(best - ours, 2), new_check=not covered))
    # features most leaders agree on come first
    gaps.sort(key=lambda g: (-g["adoption"], -g["gap"], g["label"]))

    out = a.out or os.path.join(HERE, "reports", cfg["site"].get("slug", "site"), dt.date.today().isoformat())
    os.makedirs(out, exist_ok=True)
    res = dict(run=dt.datetime.now().isoformat(timespec="minutes"), ours=us, leaders=leaders,
               virtual_best=virtual, gaps=gaps, inventory=dict(ours=us_inv, leaders=invs))
    json.dump(res, open(os.path.join(out, "benchmark.json"), "w"), indent=2, default=str)

    pct = lambda v: f"{round(v * 100)}%"
    L = [f"# Benchmark — {cfg['site']['name']}", "",
         f"This site: **{us['score']}** · " + " · ".join(f"{r['name']}: **{r['score']}**" for r in leaders), "",
         "## Virtual 100 (best leader per layer)", "", "| Layer | Ours | Best | Leader |", "|---|---|---|---|"]
    L += [f"| {k} | {v['ours']} | {v['score']} | {v['leader']} |" for k, v in virtual.items()]
    L += ["", "## What the leaders do that this site doesn't", "",
          "| Feature | Ours | Leaders | Idea | New check? |", "|---|---|---|---|---|"]
    for g in gaps:
        L.append(f"| {g['label']} | {pct(g['ours'])} | " + ", ".join(f"{n} {pct(v)}" for n, v in g["leaders"].items())
                 + f" | {g['idea']} | {'yes' if g['new_check'] else ''} |")
    open(os.path.join(out, "benchmark.md"), "w").write("\n".join(L) + "\n")
    print(f"benchmark: us {us['score']} vs leaders {[r['score'] for r in leaders]} · {len(gaps)} gaps "
          f"({sum(g['new_check'] for g in gaps)} new-check candidates) → {out}/benchmark.md")


if __name__ == "__main__":
    main()

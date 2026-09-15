#!/usr/bin/env python3
"""
SOE Audit — repeatable, config-driven search-optimisation audit for any website.

Usage:
    python soe_audit.py configs/<project>.yaml [--out reports/<project>] [--lighthouse]

Covers the automatable layers of the SOE Playbook:
  T  Technical   (HTTPS, host canonicalisation, robots, sitemap, status codes)
  O  On-page     (title, description, H1, canonical, alt text, content depth)
  S  Structured  (JSON-LD types present vs. required for the project type)
  E  Entity/NAP  (business name, phone, postcode consistent on-site)
  A  AI search   (AI crawler access, llms.txt, text-extractable content)
  P  Performance (Lighthouse lab data, optional PageSpeed/CrUX via API key)

Outputs: report.md (human) + findings.json (machine; diff runs over time).
Requires: pip install requests beautifulsoup4 lxml pyyaml
Optional: node + npx (Lighthouse), env PSI_API_KEY (PageSpeed Insights/CrUX field data)
"""
import argparse, datetime as dt, json, os, re, subprocess, sys, tempfile
from urllib.parse import urljoin, urlparse
from urllib import robotparser

import requests, yaml
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (compatible; SOE-Audit/1.0; +https://example.com/soe)"
AI_BOTS = {  # search/live-fetch bots matter for visibility; training bots are a policy choice
    "search": ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot",
               "Claude-User", "PerplexityBot", "Perplexity-User", "Applebot"],
    "training": ["GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended", "CCBot"],
}
# Schema.org types expected per project type (extend freely)
REQUIRED_SCHEMA = {
    "local_business": [["LocalBusiness", "HairSalon", "BeautySalon", "HealthAndBeautyBusiness",
                        "Restaurant", "Store", "ProfessionalService", "DaySpa", "NailSalon"]],
    "saas": [["Organization"], ["SoftwareApplication", "WebApplication", "Product"]],
    "ecommerce": [["Organization"], ["Product"]],
    "publisher": [["Organization", "NewsMediaOrganization"], ["Article", "NewsArticle", "BlogPosting"]],
    "personal_brand": [["Person", "MusicGroup", "Organization"]],
    "generic": [["Organization", "LocalBusiness", "Person"]],
}
SEV_W = {"critical": 10, "high": 6, "medium": 3, "low": 1}
HERE = os.path.dirname(os.path.abspath(__file__))


def load_yaml(*parts):
    path = os.path.join(HERE, *parts)
    return yaml.safe_load(open(path)) if os.path.exists(path) else {}


class Audit:
    def __init__(self, cfg):
        self.cfg = cfg
        self.base = cfg["site"]["url"].rstrip("/")
        self.host = urlparse(self.base).netloc
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.findings, self.pages, self.meta = [], {}, {}
        ptype = cfg["site"].get("type", "generic")
        self.module = load_yaml("modules", f"{ptype}.yaml") or load_yaml("modules", "generic.yaml")
        plat = (cfg["site"].get("platform") or "").lower()
        self.fixpack = (load_yaml("fixpacks", f"{plat}.yaml") or {}).get("fixes", {})
        self.nav = []  # (url, link text) pairs seen during the crawl

    # ---------- helpers ----------
    def add(self, layer, sev, check, detail, fix, url=None):
        how = self.fixpack.get(check) or self.fixpack.get(check.split(":")[0]) if hasattr(self, "fixpack") else None
        self.findings.append(dict(layer=layer, severity=sev, check=check, detail=detail, fix=fix, url=url, how=how))

    def get(self, url, **kw):
        try:
            return self.s.get(url, timeout=25, **kw)
        except requests.RequestException:
            return None

    # ---------- T: technical ----------
    def technical(self):
        p = urlparse(self.base)
        bare = p.netloc[4:] if p.netloc.startswith("www.") else "www." + p.netloc
        for variant in (f"http://{p.netloc}/", f"https://{bare}/", f"http://{bare}/"):
            r = self.get(variant, allow_redirects=True)
            if r is None:
                continue
            if r.url.rstrip("/") != self.base:
                self.add("T", "high", "host-canonicalisation", f"{variant} ends at {r.url}",
                         f"301 all variants to {self.base}/")
        home = self.get(self.base + "/")
        if not home or home.status_code != 200:
            self.add("T", "critical", "homepage", f"status {getattr(home,'status_code',None)}", "Fix homepage availability")
        # robots
        rb = self.get(self.base + "/robots.txt")
        self.robots_txt = rb.text if rb is not None and rb.status_code == 200 else ""
        if not self.robots_txt:
            self.add("T", "medium", "robots.txt", "missing", "Publish robots.txt with Sitemap: line")
        elif "sitemap:" not in self.robots_txt.lower():
            self.add("T", "low", "robots-sitemap", "robots.txt does not declare the sitemap", "Add 'Sitemap: <url>'")
        # sitemap
        urls = self.sitemap_urls(self.base + "/sitemap.xml")
        if not urls:
            self.add("T", "high", "sitemap", "no URLs found in /sitemap.xml", "Generate an XML sitemap and submit it in GSC/Bing")
        self.meta["sitemap_urls"] = len(urls)
        return urls

    def sitemap_urls(self, url, depth=0):
        r = self.get(url)
        if r is None or r.status_code != 200 or depth > 2:
            return []
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
        if "<sitemapindex" in r.text:
            out = []
            for l in locs:
                out += self.sitemap_urls(l, depth + 1)
            return out
        return locs

    # ---------- page crawl ----------
    def crawl(self, seeds):
        limit = self.cfg.get("audit", {}).get("max_pages", 50)
        queue, seen = [self.base + "/"] + seeds, set()
        while queue and len(self.pages) < limit:
            u = queue.pop(0).split("#")[0].split("?")[0]   # ignore query-string variants (replytocom, utm...)
            key = u.rstrip("/")
            if key in seen or urlparse(u).netloc != self.host:
                continue
            seen.add(key)
            r = self.get(u)
            if r is None:
                continue
            if r.status_code >= 400:
                self.add("T", "high", "broken-page", f"HTTP {r.status_code}", "Fix or 301 redirect", u)
                continue
            if "text/html" not in r.headers.get("content-type", ""):
                continue
            soup = BeautifulSoup(r.text, "lxml")
            self.pages[key] = self.page_facts(u, r, soup)
            for a in soup.find_all("a", href=True):
                h = urljoin(u, a["href"])
                self.nav.append((h, a.get_text(" ", strip=True)))
                if urlparse(h).netloc == self.host and not re.search(r"\.(pdf|jpg|png|zip)$|_files/", h):
                    queue.append(h)

    def page_facts(self, url, r, soup):
        def meta(name):
            m = soup.find("meta", attrs={"name": name}) or soup.find("meta", attrs={"property": name})
            return (m.get("content") or "").strip() if m else ""
        ld_types = []
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(s.string or "")
            except Exception:
                continue
            stack = data if isinstance(data, list) else [data]
            while stack:
                d = stack.pop()
                if isinstance(d, dict):
                    t = d.get("@type")
                    ld_types += t if isinstance(t, list) else ([t] if t else [])
                    stack += [v for v in d.values() if isinstance(v, (dict, list))]
                elif isinstance(d, list):
                    stack += d
        body = soup.find("body")
        text = body.get_text(" ", strip=True) if body else ""
        imgs = soup.find_all("img")
        canon = soup.find("link", rel="canonical")
        return dict(
            url=url, status=r.status_code, bytes=len(r.content),
            title=(soup.title.string or "").strip() if soup.title else "",
            description=meta("description"), robots=meta("robots"),
            og_image=meta("og:image"), og_description=meta("og:description"),
            h1=[h.get_text(" ", strip=True) for h in soup.find_all("h1")],
            h2_count=len(soup.find_all("h2")),
            canonical=canon.get("href") if canon else "",
            lang=(soup.html.get("lang") if soup.html else "") or "",
            words=len(text.split()), text=text,
            img_total=len(imgs), img_no_alt=sum(1 for i in imgs if not (i.get("alt") or "").strip()),
            ld_types=sorted(set(ld_types)),
            pdf_links=[a["href"] for a in soup.find_all("a", href=True) if ".pdf" in a["href"].lower()],
            raw_html=r.text,
        )

    # ---------- O: on-page ----------
    def onpage(self):
        titles = {}
        min_words = self.cfg.get("audit", {}).get("min_words", 300)
        for k, p in self.pages.items():
            u, t = p["url"], p["title"]
            if not t:
                self.add("O", "critical", "title", "missing title", "Write a unique 50–60 char title", u)
            else:
                titles.setdefault(t, []).append(u)
                if len(t) < 25 or len(t) > 65:
                    self.add("O", "medium", "title-length", f"{len(t)} chars: '{t}'", "Aim for 30–60 chars: primary keyword + location/brand", u)
                if re.search(r"\b(?:[A-Z] ){2,}[A-Z]\b", t) or t.isupper():
                    self.add("O", "high", "title-quality", f"spaced/all-caps title '{t}'",
                             "Use a readable keyword title, not a design label", u)
            if not p["description"]:
                self.add("O", "high", "meta-description", "missing", "Write a 140–160 char description with a call to action", u)
            if len(p["h1"]) == 0:
                self.add("O", "high", "h1", "no H1", "Add exactly one descriptive H1 containing the primary topic", u)
            elif len(p["h1"]) > 1:
                self.add("O", "low", "h1", f"{len(p['h1'])} H1s", "Use one H1 per page", u)
            if p["canonical"] and p["canonical"].rstrip("/") != k:
                self.add("O", "medium", "canonical", f"points to {p['canonical']}", "Self-reference unless intentional", u)
            if "noindex" in p["robots"].lower():
                self.add("O", "high", "noindex", "page is noindex but linked/in sitemap", "Remove noindex or drop from sitemap", u)
            if p["words"] < min_words:
                self.add("O", "medium", "thin-content", f"{p['words']} words (<{min_words})",
                         "Expand with useful, specific text (services, FAQs, proof)", u)
            ph = re.search(r"lorem ipsum|this is placeholder text|double-click on the element|add your own content|"
                           r"i'm a paragraph|click here to add your own|coming soon|hello world!|sample page|just another wordpress site|"
                           r"this is an example page", p["text"], re.I)
            if ph:
                self.add("O", "high", "placeholder-text", f"template placeholder text on page: '{ph.group(0)}'",
                         "Replace builder placeholder copy with real content (it looks unfinished to people and engines)", u)
            if p["img_no_alt"]:
                self.add("O", "low", "alt-text", f"{p['img_no_alt']}/{p['img_total']} images lack alt",
                         "Describe images; include service/location naturally", u)
            if not p["og_image"]:
                self.add("O", "low", "og-image", "no og:image", "Set a share image (1200×630)", u)
            if not p["lang"]:
                self.add("O", "low", "lang", "no <html lang>", "Set lang (e.g. en-GB)", u)
        pdfs = sorted(set(urljoin(p["url"], h) for p in self.pages.values() for h in p["pdf_links"]))
        if pdfs:
            self.add("O", "medium", "content-in-pdf", f"{len(pdfs)} PDF(s) linked site-wide — key info (e.g. prices) may be locked in PDF",
                     "Publish that content as HTML (crawlable, quotable by AI); keep PDF as a download", pdfs[0])
        for t, us in titles.items():
            if len(us) > 1:
                self.add("O", "medium", "duplicate-title", f"'{t}' on {len(us)} pages", "Make titles unique", us[0])
        squash = lambda t: re.sub(r"(?<=\b\w) (?=\w\b)", "", t).lower()   # "C O N T A C T" -> "contact"
        hay = [(u.lower(), squash(t)) for u, t in self.nav] + [(k.lower(), p["title"].lower()) for k, p in self.pages.items()]
        for label, pats in (self.module.get("expected_pages") or {}).items():
            if not any(any(pt in u or pt in t for pt in pats) for u, t in hay):
                self.add("O", "medium", "expected-page", f"no '{label}' page found (looked for: {', '.join(pats[:4])})",
                         f"Add a dedicated {label} page and link it from the navigation", self.base)
        for kw in self.cfg.get("keywords", {}).get("primary", []):
            home = self.pages.get(self.base)
            if home and kw.lower() not in (home["title"] + " " + " ".join(home["h1"])).lower():
                self.add("O", "medium", "keyword-targeting", f"primary keyword '{kw}' not in homepage title/H1",
                         "Map each primary keyword to one page and use it in title + H1", self.base)

    # ---------- S: structured data ----------
    def structured(self):
        ptype = self.cfg["site"].get("type", "generic")
        all_types = set(t for p in self.pages.values() for t in p["ld_types"])
        self.meta["schema_types"] = sorted(all_types)
        groups = self.module.get("required_schema") or REQUIRED_SCHEMA.get(ptype, REQUIRED_SCHEMA["generic"])
        for group in groups:
            if not all_types.intersection(group):
                self.add("S", "critical", "schema-missing", f"none of {group[:3]}… found (found: {sorted(all_types) or 'none'})",
                         f"Add JSON-LD for {group[0]} (see schema/ templates)", self.base)
        if all_types:
            html = " ".join(p.get("raw_html", "") for p in self.pages.values())
            for prop in self.module.get("schema_props", []):
                if prop not in html:
                    self.add("S", "medium", f"schema-{prop}", f"'{prop}' not present in any JSON-LD on the site",
                             f"Include {prop} in the main entity markup", self.base)

    # ---------- E: entity / NAP ----------
    def entity(self):
        b = self.cfg.get("business") or {}
        if not b:
            return
        home = self.pages.get(self.base, {})
        txt = " ".join(p["text"] for p in self.pages.values())
        norm = lambda s: re.sub(r"\D", "", s or "")
        if b.get("phone") and norm(b["phone"])[-9:] not in norm(txt):
            self.add("E", "high", "nap-phone", "configured phone not found on site", "Show the phone in the footer on every page")
        if b.get("postcode") and b["postcode"].replace(" ", "").lower() not in txt.replace(" ", "").lower():
            self.add("E", "high", "nap-postcode", "postcode not found on site", "Show the full address in the footer")
        name = b.get("name", "")
        if name and name.lower() not in (home.get("title", "") + home.get("text", "")[:3000]).lower():
            self.add("E", "medium", "brand-name", f"canonical name '{name}' not used consistently (title: '{home.get('title','')}')",
                     "Use one exact business name everywhere (site, GBP, directories, schema)")
        em = b.get("email", "")
        if em and urlparse(self.base).netloc.replace("www.", "") not in em:
            self.add("E", "low", "email-domain", f"email {em} is on a different domain from the site",
                     "Use an address on the site domain, or redirect the old domain to the site")
        for label, url in (b.get("profiles") or {}).items():
            if url and url not in " ".join(p["raw_html"] for p in self.pages.values()):
                self.add("E", "low", "profile-link", f"{label} profile not linked from site", "Link profiles and add them to schema sameAs")

    # ---------- A: AI search readiness ----------
    def ai(self):
        rp = robotparser.RobotFileParser()
        rp.parse(self.robots_txt.splitlines())
        blocked = {g: [b for b in bots if not rp.can_fetch(b, self.base + "/")] for g, bots in AI_BOTS.items()}
        self.meta["ai_bots_blocked"] = blocked
        if blocked["search"]:
            self.add("A", "critical", "ai-search-bots-blocked", f"blocked: {blocked['search']}",
                     "Allow search/live-fetch bots in robots.txt (also check CDN/WAF bot rules)")
        policy = self.cfg.get("ai", {}).get("allow_training", None)
        if policy is False and len(blocked["training"]) < len(AI_BOTS["training"]):
            self.add("A", "low", "ai-training-policy", "training bots allowed but policy says block",
                     "Add Disallow rules for GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot")
        r = self.get(self.base + "/llms.txt")
        has_llms = bool(r is not None and r.status_code == 200 and r.text.strip())
        self.meta["llms_txt"] = has_llms
        if not has_llms:
            self.add("A", "low", "llms.txt", "missing", "Optional: publish /llms.txt (cheap, low evidence of impact)")
        else:
            desc = r.text[:600].lower()
            focus = self.cfg.get("ai", {}).get("llms_should_mention", [])
            miss = [w for w in focus if w.lower() not in desc]
            if miss:
                self.add("A", "medium", "llms.txt-summary", f"summary does not mention {miss}",
                         "Rewrite the llms.txt summary to describe the business, not a random page")
        home = self.pages.get(self.base, {})
        if home and home.get("words", 0) < 150:
            self.add("A", "high", "extractable-text", f"homepage has {home.get('words')} words of text",
                     "AI answers quote text: add concise factual paragraphs (who/what/where/price/hours)")
        faqish = any(re.search(r"\?\s", p["text"]) for p in self.pages.values())
        if not faqish:
            self.add("A", "medium", "answer-content", "no question-style content found",
                     "Add an FAQ / Q&A section answering real customer questions (visible text, not just schema)")

    # ---------- P: performance ----------
    def performance(self, run_lh):
        key = os.environ.get("PSI_API_KEY")
        if key:
            try:
                r = self.s.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
                               params={"url": self.base + "/", "strategy": "mobile", "key": key}, timeout=120).json()
                le = r.get("loadingExperience", {}).get("metrics", {})
                self.meta["crux"] = {k: v.get("percentile") for k, v in le.items()}
            except Exception as e:
                self.meta["crux_error"] = str(e)
        if not run_lh:
            return
        runs = int(self.cfg.get("audit", {}).get("lighthouse_runs", 3))
        env = dict(os.environ)
        if not env.get("CHROME_PATH"):
            import glob
            c = glob.glob("/opt/pw-browsers/chromium*/chrome-linux/chrome")
            if c:
                env["CHROME_PATH"] = c[0]
        results = []
        for i in range(runs):
            out = os.path.join(tempfile.mkdtemp(), "lh.json")
            cmd = ["npx", "-y", "lighthouse@12", self.base + "/", "--quiet", "--output=json", f"--output-path={out}",
                   "--only-categories=performance,seo,accessibility,best-practices",
                   "--chrome-flags=--headless=new --no-sandbox"]
            try:
                subprocess.run(cmd, env=env, check=True, capture_output=True, timeout=300)
                results.append(json.load(open(out)))
            except Exception as e:
                self.meta["lighthouse_error"] = str(e)[:200]
                print("Lighthouse failed:", str(e)[:200], file=sys.stderr)
        if not results:
            return
        # lab scores vary run to run: keep the run with the median performance score
        results.sort(key=lambda d: d["categories"]["performance"]["score"] or 0)
        d = results[len(results) // 2]
        self.meta["lighthouse_runs"] = [round((r["categories"]["performance"]["score"] or 0) * 100) for r in results]
        cats = {k: round(v["score"] * 100) for k, v in d["categories"].items()}
        a = d["audits"]
        lab = {k: a[k]["numericValue"] for k in ("largest-contentful-paint", "cumulative-layout-shift", "total-blocking-time")}
        self.meta["lighthouse"] = dict(scores=cats, lab=lab)
        if lab["largest-contentful-paint"] > 2500:
            self.add("P", "high" if lab["largest-contentful-paint"] > 4000 else "medium", "lcp",
                     f"lab LCP {lab['largest-contentful-paint']/1000:.1f}s (good ≤2.5s)", "Compress/preload hero image, cut render-blocking JS")
        if lab["total-blocking-time"] > 300:
            self.add("P", "medium", "tbt-inp-proxy", f"TBT {lab['total-blocking-time']:.0f}ms (INP risk)",
                     "Remove unused apps/widgets and third-party scripts")
        if lab["cumulative-layout-shift"] > 0.1:
            self.add("P", "medium", "cls", f"CLS {lab['cumulative-layout-shift']:.2f}", "Reserve space for images/embeds")

    # ---------- scoring + report ----------
    def score(self):
        layers = {"T": "Technical", "O": "On-page", "S": "Structured data", "E": "Entity / NAP",
                  "A": "AI search readiness", "P": "Performance"}
        out = {}
        for L, name in layers.items():
            by_check = {}
            for f in self.findings:
                if f["layer"] == L:
                    c = by_check.setdefault(f["check"], [0, 0])
                    c[0] = max(c[0], SEV_W[f["severity"]]); c[1] += 1
            # a repeated issue costs more, but with diminishing returns (sqrt of occurrences, capped at 4)
            pen = sum(w * min(n, 4) ** 0.5 for w, n in by_check.values())
            out[name] = round(max(0, 100 - pen * 1.5))
        lh = self.meta.get("lighthouse", {}).get("scores", {})
        if lh.get("performance") is not None:
            out["Performance"] = min(out["Performance"], lh["performance"])
        elif "crux" not in self.meta:
            out["Performance"] = None  # not measured: excluded from the total
        weights = self.cfg.get("audit", {}).get("weights",
                  {"Technical": 20, "On-page": 20, "Structured data": 15, "Entity / NAP": 15,
                   "AI search readiness": 15, "Performance": 15})
        m = {k: w for k, w in weights.items() if out.get(k) is not None}
        total = sum(out[k] * w for k, w in m.items()) / sum(m.values())
        return round(total), out

    def report(self, outdir):
        os.makedirs(outdir, exist_ok=True)
        total, layers = self.score()
        order = sorted(self.findings, key=lambda f: -SEV_W[f["severity"]])
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        pages = [{k: v for k, v in p.items() if k not in ("text", "raw_html")} for p in self.pages.values()]
        project = dict(name=self.cfg["site"].get("name"), slug=self.cfg["site"].get("slug"),
                       type=self.cfg["site"].get("type"), platform=self.cfg["site"].get("platform"),
                       module=self.module.get("label"))
        json.dump(dict(site=self.base, run=now, project=project, score=total, layers=layers, meta=self.meta,
                       findings=order, pages=pages), open(os.path.join(outdir, "findings.json"), "w"), indent=2, default=str)
        L = [f"# SOE audit — {self.cfg['site'].get('name', self.base)}", "",
             f"Site: {self.base} · Run: {now} · Pages crawled: {len(self.pages)} · Sitemap URLs: {self.meta.get('sitemap_urls')}", "",
             f"## Score: {total}/100", "", "| Layer | Score |", "|---|---|"]
        L += [f"| {k} | {'n/a (run with --lighthouse)' if v is None else v} |" for k, v in layers.items()]
        if "lighthouse" in self.meta:
            lh = self.meta["lighthouse"]
            L += ["", "Lighthouse (mobile lab): " + ", ".join(f"{k} {v}" for k, v in lh["scores"].items()) +
                  f" · LCP {lh['lab']['largest-contentful-paint']/1000:.1f}s · TBT {lh['lab']['total-blocking-time']:.0f}ms"
                  f" · CLS {lh['lab']['cumulative-layout-shift']:.2f}"]
        L += ["", f"Schema types found: {', '.join(self.meta.get('schema_types') or []) or 'none'}",
              f"AI bots blocked: {self.meta.get('ai_bots_blocked')} · llms.txt: {self.meta.get('llms_txt')}", "",
              "## Findings (most severe first)", "", "| Sev | Layer | Check | Detail | Fix | URL |", "|---|---|---|---|---|---|"]
        esc = lambda s: str(s or "").replace("|", "/")
        for f in order:
            L.append(f"| {f['severity']} | {f['layer']} | {f['check']} | {esc(f['detail'])} | {esc(f['fix'])} | {esc(f['url']).replace(self.base, '') or '/'} |")
        steps = {}
        for f in order:
            if f.get("how") and f["check"] not in steps:
                steps[f["check"]] = f["how"]
        if steps:
            L += ["", f"## How to fix on {self.cfg['site'].get('platform', 'this platform')}", ""]
            L += [f"- **{k}** — {v}" for k, v in steps.items()]
        L += ["", "## Pages", "", "| URL | Title | Desc | H1 | Words | Schema |", "|---|---|---|---|---|---|"]
        for p in pages:
            L.append(f"| {p['url'].replace(self.base, '') or '/'} | {esc(p['title'])} | {'✓' if p['description'] else '✗'} | "
                     f"{len(p['h1'])} | {p['words']} | {', '.join(p['ld_types'])} |")
        L += ["", "_Manual layers not covered by this script: Google Business Profile, reviews, citations, "
              "backlinks, rankings, AI-answer visibility — see PLAYBOOK.md §4._"]
        open(os.path.join(outdir, "report.md"), "w").write("\n".join(L) + "\n")
        return total


def run_audit(cfg, lighthouse=False):
    au = Audit(cfg)
    seeds = au.technical()
    au.crawl(seeds)
    au.onpage(); au.structured(); au.entity(); au.ai(); au.performance(lighthouse)
    return au


def benchmark(cfg, out):
    """Light audit of each competitor URL (no business block, 10 pages) -> competitors.json."""
    rows = []
    for c in cfg.get("competitors") or []:
        if not isinstance(c, dict) or not c.get("url"):
            continue
        ccfg = {"site": {"name": c.get("name"), "url": c["url"], "type": cfg["site"].get("type", "generic")},
                "audit": {"max_pages": 10, "min_words": cfg.get("audit", {}).get("min_words", 300)}}
        try:
            au = run_audit(ccfg)
            total, layers = au.score()
            home = au.pages.get(au.base, {})
            rows.append(dict(name=c.get("name"), url=c["url"], score=total, layers=layers, pages=len(au.pages),
                             findings=len(au.findings), schema=au.meta.get("schema_types"),
                             home_title=home.get("title"), home_words=home.get("words")))
            print(f"  benchmark {c.get('name')}: {total}")
        except Exception as e:  # a competitor site failing must not break the run
            rows.append(dict(name=c.get("name"), url=c["url"], error=str(e)[:200]))
    json.dump(rows, open(os.path.join(out, "competitors.json"), "w"), indent=2, default=str)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out")
    ap.add_argument("--lighthouse", action="store_true", help="run Lighthouse (needs node/npx + Chrome)")
    ap.add_argument("--competitors", action="store_true", help="also audit competitor URLs from the config")
    ap.add_argument("--integrations", action="store_true", help="run key-gated API integrations")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    au = run_audit(cfg, a.lighthouse)
    out = a.out or os.path.join(HERE, "reports", cfg["site"].get("slug", "site"), dt.date.today().isoformat())
    score = au.report(out)
    print(f"SOE score {score}/100 · {len(au.findings)} findings · report: {out}/report.md")
    if a.competitors:
        benchmark(cfg, out)
    if a.integrations:
        sys.path.insert(0, HERE)
        from integrations import run_all
        run_all.run(cfg, out)


if __name__ == "__main__":
    main()

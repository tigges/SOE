#!/usr/bin/env python3
"""
Add a site to the SOE kit: write configs/<slug>.yaml from a few fields.

Usage:
    python soe_add_site.py --name "Example Co" --url https://www.example.com \\
        --type local_business --platform wix
    python soe_add_site.py --name "Example Co" --url https://www.example.com --print

The Control Room "Add site" button produces the same settings file. The
"Add site" GitHub Action runs this script, then the first audit.
"""
import argparse, json, os, re, sys
from urllib.parse import urlparse

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
TYPES = ["local_business", "saas", "ecommerce", "publisher", "personal_brand", "generic"]
PLATFORMS = ["wix", "wordpress", "webflow", "shopify", "nextjs", "other"]
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{0,47}$")


def quote(value):
    """YAML scalar: plain when safe, JSON-quoted otherwise."""
    s = "" if value is None else str(value)
    if s == "" or re.search(r"""[:#{}[\],&*?|!<>=%@`'"\\]|^\s|\s$|^[-?~]""", s) or s.lower() in (
            "true", "false", "null", "yes", "no", "on", "off"):
        return json.dumps(s)
    return s


def normalise_url(url):
    u = (url or "").strip()
    if not u:
        raise ValueError("URL is required")
    if not re.match(r"^https?://", u, re.I):
        u = "https://" + u
    p = urlparse(u)
    host = (p.hostname or "")
    if p.scheme not in ("http", "https") or not host or " " in u or "." not in host:
        raise ValueError(f"not a valid http(s) URL: {url}")
    return u.rstrip("/")


def slugify(name, url, explicit=None):
    if explicit:
        s = explicit.strip().lower()
    else:
        host = (urlparse(url).hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        s = host.split(".")[0] if host else ""
        if not s:
            s = name or ""
        s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    s = re.sub(r"[^a-z0-9-]", "", s.lower()).strip("-")
    if not s or not SLUG_RE.match(s):
        raise ValueError("slug must start with a letter and be lowercase letters, digits or hyphens")
    return s


def split_keywords(raw):
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(k).strip() for k in raw if str(k).strip()]
    return [p.strip() for p in str(raw).replace(";", ",").split(",") if p.strip()]


def existing_slugs(root):
    cfg_dir = os.path.join(root, "configs")
    if not os.path.isdir(cfg_dir):
        return set()
    out = set()
    for name in os.listdir(cfg_dir):
        if name.endswith(".yaml") and not name.startswith("_"):
            out.add(name[:-5])
    return out


def build_config(name, url, type_, platform, slug=None, description="",
                 keywords=None, location="", business_name="", phone="",
                 email="", postcode="", address=""):
    url = normalise_url(url)
    name = (name or "").strip()
    if not name:
        raise ValueError("name is required")
    if type_ not in TYPES:
        raise ValueError(f"type must be one of: {', '.join(TYPES)}")
    if platform not in PLATFORMS:
        raise ValueError(f"platform must be one of: {', '.join(PLATFORMS)}")
    slug = slugify(name, url, slug)
    host = (urlparse(url).hostname or "").lower().removeprefix("www.")
    kw = split_keywords(keywords)
    biz_name = (business_name or name).strip()
    cfg = {
        "site": {
            "name": name,
            "slug": slug,
            "url": url,
            "type": type_,
            "platform": platform,
            "market": "en-GB",
            "description": (description or "").strip(),
            "location": (location or "").strip(),
            "gsc_property": f"sc-domain:{host}" if host else "",
        },
        "business": {
            "name": biz_name,
            "phone": (phone or "").strip(),
            "email": (email or "").strip(),
            "address": (address or "").strip(),
            "postcode": (postcode or "").strip(),
            "profiles": {"google_business": "", "instagram": "", "facebook": "", "booking": ""},
        },
        "keywords": {"primary": kw, "secondary": [], "questions": []},
        "competitors": [],
        "legacy_sites": [],
        "name_clashes": [],
        "benchmarks": [],
        "citations": [],
        "ai": {
            "allow_training": True,
            "llms_should_mention": [],
            "prompts": [],
            "engines": ["Claude", "Google AI Mode"],
            "brand_terms": [],
        },
        "audit": {
            "max_pages": 50,
            "min_words": 300,
            "weights": {"Technical": 20, "On-page": 20, "Structured data": 15,
                        "Entity / NAP": 15, "AI search readiness": 15, "Performance": 15},
        },
    }
    return cfg


def render_yaml(cfg):
    s, b, k = cfg["site"], cfg["business"], cfg["keywords"]
    primary = k.get("primary") or []
    kw_lines = ["  primary: []"] if not primary else ["  primary:"] + [f"    - {quote(t)}" for t in primary]
    lines = [
        "# SOE project config — drafted by soe_add_site.py. Fill in the blanks, then run the audit.",
        "site:",
        f"  name: {quote(s['name'])}",
        f"  slug: {s['slug']}",
        f"  url: {s['url']}",
        f"  type: {s['type']}                   # local_business | saas | ecommerce | publisher | personal_brand | generic",
        f"  platform: {s['platform']}                    # wix | wordpress | webflow | shopify | nextjs | other",
        f"  market: {s.get('market') or 'en-GB'}",
        f"  description: {quote(s.get('description') or '')}",
        f"  location: {quote(s.get('location') or '')}   # for rank tracking, e.g. London,England,United Kingdom",
        f"  gsc_property: {quote(s.get('gsc_property') or '')}",
        "",
        "business:",
        f"  name: {quote(b.get('name') or s['name'])}",
        f"  phone: {quote(b.get('phone') or '')}",
        f"  email: {quote(b.get('email') or '')}",
        f"  address: {quote(b.get('address') or '')}",
        f"  postcode: {quote(b.get('postcode') or '')}",
        "  profiles:",
        "    google_business: \"\"",
        "    instagram: \"\"",
        "    facebook: \"\"",
        "    booking: \"\"",
        "",
        "keywords:",
        *kw_lines,
        "  secondary: []",
        "  questions: []                          # real customer questions -> FAQ / answer content",
        "",
        "competitors: []                          # {name, url} — audited with --competitors",
        "legacy_sites: []                         # old/parked sites to take offline or redirect",
        "name_clashes: []                         # other businesses with a similar name",
        "benchmarks: []                           # best-in-class leaders (soe_benchmark.py --discover)",
        "citations: []                            # off-site listings checked by soe_citations.py",
        "",
        "ai:",
        "  allow_training: true",
        "  llms_should_mention: []",
        "  prompts: []                            # monthly tests in Claude (auto) and Google AI Mode (manual)",
        "  engines: [Claude, Google AI Mode]",
        "  brand_terms: []",
        "",
        "audit:",
        "  max_pages: 50",
        "  min_words: 300",
        "  weights: {Technical: 20, On-page: 20, Structured data: 15, Entity / NAP: 15, AI search readiness: 15, Performance: 15}",
        "",
    ]
    return "\n".join(lines)


def write_site(cfg, root, force=False):
    slug = cfg["site"]["slug"]
    cfg_dir = os.path.join(root, "configs")
    path = os.path.join(cfg_dir, f"{slug}.yaml")
    os.makedirs(cfg_dir, exist_ok=True)
    if os.path.exists(path) and not force:
        raise FileExistsError(f"configs/{slug}.yaml already exists (pass --force to replace it)")
    with open(path, "w") as f:
        f.write(render_yaml(cfg))
    os.makedirs(os.path.join(root, "projects", slug), exist_ok=True)
    os.makedirs(os.path.join(root, "data", slug), exist_ok=True)
    with open(path) as f:
        yaml.safe_load(f)  # fail fast if the file isn't valid YAML
    return path


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="Add a site to the SOE kit (writes configs/<slug>.yaml).")
    ap.add_argument("--name", required=True, help="Site or brand name")
    ap.add_argument("--url", required=True, help="Canonical origin, e.g. https://www.example.com")
    ap.add_argument("--type", dest="type_", required=True, choices=TYPES)
    ap.add_argument("--platform", required=True, choices=PLATFORMS)
    ap.add_argument("--slug", help="Folder/settings-file name (default: first label of the host)")
    ap.add_argument("--description", default="", help="One factual sentence: what, where, for whom")
    ap.add_argument("--keywords", default="", help="Comma-separated primary keywords")
    ap.add_argument("--location", default="", help="Rank-tracking location, e.g. London,England,United Kingdom")
    ap.add_argument("--business-name", default="", help="Canonical business name if it differs from --name")
    ap.add_argument("--phone", default="")
    ap.add_argument("--email", default="")
    ap.add_argument("--postcode", default="")
    ap.add_argument("--address", default="")
    ap.add_argument("--root", default=HERE, help="Kit root (default: this repo)")
    ap.add_argument("--force", action="store_true", help="Overwrite an existing settings file")
    ap.add_argument("--print", dest="print_only", action="store_true",
                    help="Print the settings file and do not write it")
    return ap.parse_args(argv)


def main(argv=None):
    a = parse_args(argv)
    try:
        cfg = build_config(
            a.name, a.url, a.type_, a.platform, slug=a.slug, description=a.description,
            keywords=a.keywords, location=a.location, business_name=a.business_name,
            phone=a.phone, email=a.email, postcode=a.postcode, address=a.address,
        )
        slug = cfg["site"]["slug"]
        if not a.print_only and slug in existing_slugs(a.root) and not a.force:
            raise FileExistsError(f"configs/{slug}.yaml already exists (pass --force to replace it)")
        text = render_yaml(cfg)
        if a.print_only:
            sys.stdout.write(text)
            return 0
        path = write_site(cfg, a.root, force=a.force)
    except (ValueError, FileExistsError) as e:
        print(f"soe_add_site: {e}", file=sys.stderr)
        return 2
    rel = os.path.relpath(path, a.root)
    print(f"wrote {rel}")
    print(f"slug: {slug}")
    if os.environ.get("GITHUB_ENV"):
        open(os.environ["GITHUB_ENV"], "a").write(f"SLUG={slug}\n")
    print(f"Next: python soe_audit.py {rel} --out reports/{slug}/$(date +%F) --lighthouse")
    print(f"  or: GitHub → Actions → SOE run → site = {slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

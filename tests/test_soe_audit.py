#!/usr/bin/env python3
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import soe_audit as audit


class SplitSiteUrl(unittest.TestCase):
    def test_apex(self):
        origin, query, home = audit.split_site_url("https://www.yuzuhairandbeauty.london")
        self.assertEqual(origin, "https://www.yuzuhairandbeauty.london")
        self.assertEqual(query, "")
        self.assertEqual(home, "https://www.yuzuhairandbeauty.london/")

    def test_github_pages_clean_variant(self):
        origin, query, home = audit.split_site_url("https://tigges.github.io/YUZU_SEPT_26/?v=clean")
        self.assertEqual(origin, "https://tigges.github.io/YUZU_SEPT_26")
        self.assertEqual(query, "v=clean")
        self.assertEqual(home, "https://tigges.github.io/YUZU_SEPT_26/?v=clean")

    def test_path_trailing_slash(self):
        origin, query, home = audit.split_site_url("https://tigges.github.io/YUZU_SEPT_26/")
        self.assertEqual(origin, "https://tigges.github.io/YUZU_SEPT_26")
        self.assertEqual(home, "https://tigges.github.io/YUZU_SEPT_26/")


class AuditUsesHomeUrl(unittest.TestCase):
    def test_query_variant_does_not_pollute_robots_path(self):
        au = audit.Audit({"site": {"url": "https://tigges.github.io/YUZU_SEPT_26/?v=clean", "type": "local_business"}})
        self.assertEqual(au.base, "https://tigges.github.io/YUZU_SEPT_26")
        self.assertEqual(au.home, "https://tigges.github.io/YUZU_SEPT_26/?v=clean")
        self.assertEqual(au.base + "/robots.txt", "https://tigges.github.io/YUZU_SEPT_26/robots.txt")


if __name__ == "__main__":
    unittest.main()

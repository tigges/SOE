#!/usr/bin/env python3
import json, os, sys, tempfile, unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import soe_citations as cit


BIZ = {"name": "Yuzu Hair & Beauty", "phone": "020 8840 2244", "postcode": "W5 2TD"}
NAMES = ["Yuzu Hair & Beauty", "Yuzu Hair"]


class CheckFlags(unittest.TestCase):
    def test_ignore_skips_fetch(self):
        with mock.patch.object(cit.requests, "get") as get:
            row = cit.check({
                "source": "beautynailhairsalons.com",
                "url": "https://www.beautynailhairsalons.com/GB/London/listing",
                "ignore": True,
                "note": "Singapore aggregator",
            }, BIZ, NAMES)
        get.assert_not_called()
        self.assertEqual(row["status"], "ignore")
        self.assertIn("skip", row["detail"].lower())

    def test_unrelated_alias(self):
        row = cit.check({"source": "Other Co", "url": "https://example.com/x", "unrelated": True}, BIZ, NAMES)
        self.assertEqual(row["status"], "ignore")

    def test_action_list_is_todo(self):
        with mock.patch.object(cit.requests, "get") as get:
            row = cit.check({
                "source": "Google Business Profile",
                "url": "https://business.google.com/",
                "directory": "core",
                "action": "list",
                "note": "set website to the .london URL",
            }, BIZ, NAMES)
        get.assert_not_called()
        self.assertEqual(row["status"], "todo")
        self.assertEqual(row["action"], "list")

    def test_missing_url_is_todo(self):
        row = cit.check({"source": "Bing Places", "directory": "core"}, BIZ, NAMES)
        self.assertEqual(row["status"], "todo")
        self.assertEqual(row["url"], "")

    def test_manual_still_skips_fetch(self):
        with mock.patch.object(cit.requests, "get") as get:
            row = cit.check({
                "source": "Instagram",
                "url": "https://www.instagram.com/yuzuhairandbeauty/",
                "manual": True,
            }, BIZ, NAMES)
        get.assert_not_called()
        self.assertEqual(row["status"], "manual")


class Gaps(unittest.TestCase):
    DIRS = {
        "core": ["Google Business Profile", "Bing Places", "Facebook"],
        "uk_general": ["Yell", "Thomson Local"],
    }

    def test_ignore_does_not_fill_a_gap(self):
        rows = [cit.check({
            "source": "beautynailhairsalons.com",
            "url": "https://www.beautynailhairsalons.com/x",
            "ignore": True,
        }, BIZ, NAMES)]
        gaps = cit.directory_gaps(self.DIRS, rows)
        self.assertIn("Google Business Profile", gaps["core"])
        self.assertIn("Yell", gaps["uk_general"])

    def test_todo_fills_named_directory(self):
        rows = [
            cit.check({"source": "Google Business Profile", "url": "https://business.google.com/",
                       "action": "list"}, BIZ, NAMES),
            cit.check({"source": "Facebook", "url": "https://facebook.com/yuzu", "manual": True}, BIZ, NAMES),
        ]
        gaps = cit.directory_gaps(self.DIRS, rows)
        self.assertNotIn("Google Business Profile", gaps.get("core", []))
        self.assertIn("Bing Places", gaps["core"])
        self.assertNotIn("Facebook", gaps["core"])


class Markdown(unittest.TestCase):
    def test_source_md_links_http(self):
        self.assertEqual(
            cit.source_md({"source": "Yell", "url": "https://www.yell.com/biz/x"}),
            "[Yell](https://www.yell.com/biz/x)",
        )

    def test_source_md_plain_without_url(self):
        self.assertEqual(cit.source_md({"source": "Bing Places", "url": ""}), "Bing Places")


class EndToEnd(unittest.TestCase):
    def test_main_writes_todo_and_ignore(self):
        cfg = """
site: {name: "Yuzu Hair & Beauty", slug: yuzu, url: https://www.yuzuhairandbeauty.london, type: local_business}
business: {name: "Yuzu Hair & Beauty", phone: "020 8840 2244", postcode: "W5 2TD"}
citations:
  - {source: Google Business Profile, url: "https://business.google.com/", directory: core, action: list, note: "add .london URL"}
  - {source: beautynailhairsalons.com, url: "https://www.beautynailhairsalons.com/x", ignore: true, note: "Singapore"}
  - {source: Facebook, url: "https://www.facebook.com/YUZUHairandBeauty/", directory: core, manual: true}
"""
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = os.path.join(tmp, "yuzu.yaml")
            open(cfg_path, "w").write(cfg)
            out = os.path.join(tmp, "out")
            with mock.patch.object(sys, "argv", ["soe_citations.py", cfg_path, "--out", out]):
                cit.main()
            data = json.load(open(os.path.join(out, "citations.json")))
            statuses = {r["source"]: r["status"] for r in data["listings"]}
            self.assertEqual(statuses["Google Business Profile"], "todo")
            self.assertEqual(statuses["beautynailhairsalons.com"], "ignore")
            self.assertEqual(statuses["Facebook"], "manual")
            self.assertEqual(data["summary"]["todo"], 1)
            self.assertEqual(data["summary"]["ignore"], 1)
            md = open(os.path.join(out, "citations.md")).read()
            self.assertIn("todo", md)
            self.assertIn("ignore", md)
            self.assertNotIn("Google Business Profile", " ".join(data["gaps"].get("core", [])))


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
import os, sys, tempfile, unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations import indexnow as inn


class IndexNow(unittest.TestCase):
    def test_key_location_default(self):
        self.assertEqual(
            inn.key_location("https://djurbant.com", "abc123def"),
            "https://djurbant.com/abc123def.txt",
        )

    def test_key_location_full_url(self):
        self.assertEqual(
            inn.key_location("https://djurbant.com", "abc", "https://www.djurbant.com/indexnow.txt"),
            "https://www.djurbant.com/indexnow.txt",
        )

    def test_key_location_path(self):
        self.assertEqual(
            inn.key_location("https://www.tigg3s.com", "abc", "keys/indexnow.txt"),
            "https://www.tigg3s.com/keys/indexnow.txt",
        )

    def test_wix_skip(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"INDEXNOW_KEY": "abcd1234efgh5678"}):
                out = inn.run({"site": {"url": "https://www.yuzuhairandbeauty.london", "platform": "wix"}}, tmp)
            self.assertEqual(out["skipped"][:12], "not possible")
            self.assertTrue(os.path.isfile(os.path.join(tmp, "indexnow.json")))

    def test_missing_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"INDEXNOW_KEY": ""}):
                self.assertIsNone(inn.run({"site": {"url": "https://djurbant.com", "platform": "wordpress"}}, tmp))


if __name__ == "__main__":
    unittest.main()

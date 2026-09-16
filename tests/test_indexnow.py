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
            with mock.patch.dict(os.environ, {"INDEXNOW_KEY": "", "INDEXNOW_URL_TXT": ""}, clear=False):
                self.assertIsNone(inn.run({"site": {"url": "https://djurbant.com", "platform": "wordpress"}}, tmp))

    def test_resolve_key_from_url_txt_hex(self):
        key = "a" * 32
        with mock.patch.dict(os.environ, {"INDEXNOW_KEY": "", "INDEXNOW_URL_TXT": key}, clear=False):
            self.assertEqual(inn.resolve_key(), (key, None))

    def test_resolve_key_from_keyfile_url(self):
        loc = "https://djurbant.com/abcd1234efgh5678.txt"
        with mock.patch.dict(os.environ, {"INDEXNOW_KEY": "", "INDEXNOW_URL_TXT": loc}, clear=False):
            self.assertEqual(inn.resolve_key(), ("abcd1234efgh5678", loc))

    def test_resolve_key_prefers_indexnow_key(self):
        with mock.patch.dict(os.environ, {"INDEXNOW_KEY": "primarykey12", "INDEXNOW_URL_TXT": "https://x.example/other.txt"}, clear=False):
            self.assertEqual(inn.resolve_key(), ("primarykey12", "https://x.example/other.txt"))


if __name__ == "__main__":
    unittest.main()

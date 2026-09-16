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

    def test_hosted_key_location_prefers_indexnow_txt(self):
        class Fake:
            def __init__(self, mapping):
                self.mapping = mapping
            def get(self, url, timeout=20):
                body = self.mapping.get(url)
                r = mock.Mock()
                if body is None:
                    r.ok = False
                    r.text = ""
                    return r
                r.ok = True
                r.text = body
                return r
        key = "abcd1234efgh5678"
        loc = inn.hosted_key_location(
            Fake({"https://www.yuzuhairandbeauty.london/indexnow.txt": key}),
            "https://www.yuzuhairandbeauty.london", key, None,
        )
        self.assertEqual(loc, "https://www.yuzuhairandbeauty.london/indexnow.txt")

    def test_wix_submits_when_sitemap_has_urls(self):
        with tempfile.TemporaryDirectory() as tmp:
            resp = mock.Mock(status_code=202, reason="Accepted", text="")
            def fake_get(url, timeout=20):
                r = mock.Mock()
                if url.endswith("sitemap.xml"):
                    r.ok, r.text = True, "<urlset><loc>https://www.yuzuhairandbeauty.london/</loc></urlset>"
                elif url.endswith("indexnow.txt"):
                    r.ok, r.text = True, "abcd1234efgh5678"
                else:
                    r.ok, r.text = False, ""
                return r
            with mock.patch.dict(os.environ, {"INDEXNOW_KEY": "abcd1234efgh5678", "INDEXNOW_URL_TXT": ""}, clear=False):
                with mock.patch.object(inn.requests.Session, "get", side_effect=fake_get), \
                     mock.patch.object(inn.requests.Session, "post", return_value=resp):
                    out = inn.run({"site": {"url": "https://www.yuzuhairandbeauty.london", "platform": "wix"}}, tmp)
            self.assertEqual(out["status"], 202)
            self.assertEqual(out["submitted"], 1)
            self.assertTrue(out["key_location"].endswith("/indexnow.txt"))

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

    def test_rewrite_www_to_apex(self):
        self.assertEqual(
            inn.rewrite_to_host("http://www.tigg3s.com/about", "tigg3s.com"),
            "https://tigg3s.com/about",
        )
        self.assertIsNone(inn.rewrite_to_host("https://djurbant.com/", "tigg3s.com"))

    def test_homepage_when_sitemap_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            resp = mock.Mock(status_code=202, reason="Accepted", text="")
            def fake_get(url, timeout=20):
                r = mock.Mock()
                r.ok, r.text = False, ""
                return r
            with mock.patch.dict(os.environ, {"INDEXNOW_KEY": "abcd1234efgh5678", "INDEXNOW_URL_TXT": ""}, clear=False):
                with mock.patch.object(inn.requests.Session, "get", side_effect=fake_get), \
                     mock.patch.object(inn.requests.Session, "post", return_value=resp) as post:
                    out = inn.run({"site": {"url": "https://tigg3s.com", "platform": "other"}}, tmp)
            self.assertEqual(out["status"], 202)
            self.assertEqual(out["submitted"], 1)
            body = post.call_args.kwargs.get("json") or post.call_args[1].get("json")
            self.assertEqual(body["urlList"], ["https://tigg3s.com/"])

    def test_resolve_key_prefers_indexnow_key(self):
        with mock.patch.dict(os.environ, {"INDEXNOW_KEY": "primarykey12", "INDEXNOW_URL_TXT": "https://x.example/other.txt"}, clear=False):
            self.assertEqual(inn.resolve_key(), ("primarykey12", "https://x.example/other.txt"))


if __name__ == "__main__":
    unittest.main()

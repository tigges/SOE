#!/usr/bin/env python3
import os, sys, unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import soe_fixes as fx


class ParseDrafts(unittest.TestCase):
    def test_parse_json_array(self):
        pages = [{"url": "https://example.com/", "title": "Home"}]
        rows = fx.parse_draft_rows(
            'Here is the pack:\n[{"url":"https://example.com/","title":"Example | Brand","description":"Hi","h1":"Example"}]\n',
            pages, "Gemini draft",
        )
        self.assertEqual(rows[0]["source"], "Gemini draft")
        self.assertEqual(rows[0]["current_title"], "Home")


class LlmPrefersGemini(unittest.TestCase):
    def test_gemini_used_when_both_keys_present(self):
        cfg = {"site": {"name": "Ex", "url": "https://example.com", "type": "generic"}, "business": {}, "keywords": {}}
        pages = [{"url": "https://example.com/", "title": "Home", "description": "", "h1": ["Home"], "words": 10}]
        with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "g", "ANTHROPIC_API_KEY": "c"}, clear=False):
            with mock.patch.object(fx, "gemini_drafts", return_value=[{"url": "https://example.com/", "source": "Gemini draft"}]) as g, \
                 mock.patch.object(fx, "claude_drafts") as c:
                out = fx.llm_drafts(cfg, pages, [])
        self.assertEqual(out[0]["source"], "Gemini draft")
        g.assert_called_once()
        c.assert_not_called()

    def test_claude_when_gemini_missing(self):
        cfg = {"site": {"name": "Ex", "url": "https://example.com", "type": "generic"}, "business": {}, "keywords": {}}
        pages = [{"url": "https://example.com/", "title": "Home", "description": "", "h1": ["Home"], "words": 10}]
        with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "", "GOOGLE_API_KEY": "", "GOOGLE_GEMINI_API_KEY": "",
                                          "GOOGLE_GENAI_API_KEY": "", "ANTHROPIC_API_KEY": "c"}, clear=False):
            with mock.patch.object(fx, "gemini_drafts") as g, \
                 mock.patch.object(fx, "claude_drafts", return_value=[{"source": "Claude draft"}]) as c:
                out = fx.llm_drafts(cfg, pages, [])
        self.assertEqual(out[0]["source"], "Claude draft")
        g.assert_not_called()
        c.assert_called_once()


if __name__ == "__main__":
    unittest.main()

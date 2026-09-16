#!/usr/bin/env python3
import os, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import soe_ai_log as ai


class ClaudeParse(unittest.TestCase):
    def test_text_and_citation_urls(self):
        text, sources = ai.claude_text_and_sources({
            "content": [
                {"type": "web_search_tool_result",
                 "content": [{"type": "web_search_result", "url": "https://www.yuzuhairandbeauty.london/"}]},
                {"type": "text", "text": "Yuzu Hair & Beauty is a salon in Ealing.",
                 "citations": [{"type": "web_search_result_location",
                                "url": "https://www.yuzuhairandbeauty.london/about"}]},
            ]
        })
        self.assertIn("Yuzu Hair", text)
        self.assertEqual(
            sources,
            ["https://www.yuzuhairandbeauty.london/", "https://www.yuzuhairandbeauty.london/about"],
        )

    def test_empty_payload(self):
        self.assertEqual(ai.claude_text_and_sources({}), ("", []))
        self.assertEqual(ai.claude_text_and_sources({"content": ["nope"]}), ("", []))


class GeminiParse(unittest.TestCase):
    def test_text_and_grounding_urls(self):
        text, sources = ai.gemini_text_and_sources({
            "candidates": [{
                "content": {"parts": [{"text": "Yuzu Hair & Beauty is a salon in Ealing."}]},
                "groundingMetadata": {"groundingChunks": [
                    {"web": {"uri": "https://www.yuzuhairandbeauty.london/", "title": "Yuzu"}},
                ]},
                "citationMetadata": {"citationSources": [
                    {"uri": "https://www.yuzuhairandbeauty.london/about"},
                ]},
            }]
        })
        self.assertIn("Yuzu Hair", text)
        self.assertEqual(
            sources,
            ["https://www.yuzuhairandbeauty.london/", "https://www.yuzuhairandbeauty.london/about"],
        )

    def test_skips_thought_parts(self):
        text, sources = ai.gemini_text_and_sources({
            "candidates": [{"content": {"parts": [
                {"thought": True, "text": "thinking"},
                {"text": "visible answer"},
            ]}}]
        })
        self.assertEqual(text, "visible answer")
        self.assertEqual(sources, [])

    def test_empty_payload(self):
        self.assertEqual(ai.gemini_text_and_sources({}), ("", []))


class FirstEnv(unittest.TestCase):
    def test_gemini_key_aliases(self):
        from unittest import mock
        with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "", "GOOGLE_API_KEY": "abc"}, clear=False):
            self.assertEqual(ai.first_env(*ai.GEMINI_KEYS), "abc")
        with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "from-studio", "GOOGLE_API_KEY": "other"}, clear=False):
            self.assertEqual(ai.first_env(*ai.GEMINI_KEYS), "from-studio")


class Upsert(unittest.TestCase):
    def test_fills_blank_same_month(self):
        rows = [dict(date="2026-09-01", engine="Claude", prompt="who is X", mentioned="", cited="")]
        ai.upsert_row(rows, dict(date="2026-09-16", engine="Claude", prompt="who is X",
                                 mentioned="y", cited="n", method="api"))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["mentioned"], "y")
        self.assertEqual(rows[0]["date"], "2026-09-16")

    def test_appends_when_already_filled(self):
        rows = [dict(date="2026-09-01", engine="Claude", prompt="who is X", mentioned="n")]
        ai.upsert_row(rows, dict(date="2026-09-16", engine="Claude", prompt="who is X", mentioned="y"))
        self.assertEqual(len(rows), 2)


class SummaryPending(unittest.TestCase):
    def test_pending_only_counts_configured_engines(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = os.path.join(tmp, "data", "site")
            os.makedirs(data)
            path = os.path.join(data, "ai_log.csv")
            with open(path, "w", newline="") as f:
                f.write("date,engine,prompt,mentioned,cited,position,cited_sources,notes,method\n")
                f.write("2026-09-15,Claude,who is X,,,,,,manual\n")
                f.write("2026-09-15,Perplexity,who is X,,,,,,manual\n")
                f.write("2026-09-15,Google AI Mode,who is X,,,,,,manual\n")
            orig = ai.HERE
            ai.HERE = tmp
            try:
                cfg = {"site": {"url": "https://example.com", "slug": "site"},
                       "ai": {"engines": ["Claude", "Google AI Mode"], "prompts": ["who is X"]}}
                res = ai.summary(cfg, None)
            finally:
                ai.HERE = orig
            self.assertEqual(res["pending_checks"], 2)
            self.assertEqual(res["engines"], ["Claude", "Google AI Mode"])


class RunClaude(unittest.TestCase):
    def test_run_fills_claude_and_skips_manual_engines(self):
        import yaml
        from unittest import mock
        cfg = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "configs", "yuzu.yaml")))
        orig = ai.HERE
        with tempfile.TemporaryDirectory() as tmp:
            ai.HERE = tmp
            os.makedirs(os.path.join(tmp, "data", "yuzu"))
            os.environ["ANTHROPIC_API_KEY"] = "test-key"
            def fake(prompt, key):
                return "Yuzu Hair & Beauty in Ealing.", ["https://www.yuzuhairandbeauty.london/"]
            try:
                with mock.patch.object(ai, "ask_claude", fake):
                    ai.init(cfg)
                    ai.run(cfg)
                import csv
                rows = list(csv.DictReader(open(os.path.join(tmp, "data", "yuzu", "ai_log.csv"))))
            finally:
                ai.HERE = orig
                os.environ.pop("ANTHROPIC_API_KEY", None)
        claude = [r for r in rows if r["engine"] == "Claude"]
        self.assertEqual(len(claude), 4)
        self.assertTrue(all(r["mentioned"] == "y" and r["cited"] == "y" and r["method"] == "api" for r in claude))
        self.assertTrue(all(not r["mentioned"] for r in rows if r["engine"] == "Google AI Mode"))
        self.assertTrue(all(not r["mentioned"] for r in rows if r["engine"] == "Gemini"))


class RunGemini(unittest.TestCase):
    def test_run_fills_gemini_from_google_api_key_alias(self):
        import yaml, csv
        from unittest import mock
        cfg = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "configs", "yuzu.yaml")))
        orig = ai.HERE
        with tempfile.TemporaryDirectory() as tmp:
            ai.HERE = tmp
            os.makedirs(os.path.join(tmp, "data", "yuzu"))
            with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "", "GEMINI_API_KEY": "", "GOOGLE_API_KEY": "g-key"}, clear=False):
                def fake(prompt, key):
                    self.assertEqual(key, "g-key")
                    return "Yuzu Hair & Beauty in Ealing.", ["https://www.yuzuhairandbeauty.london/"]
                try:
                    with mock.patch.object(ai, "ask_gemini", fake):
                        ai.init(cfg)
                        ai.run(cfg)
                    rows = list(csv.DictReader(open(os.path.join(tmp, "data", "yuzu", "ai_log.csv"))))
                finally:
                    ai.HERE = orig
        gem = [r for r in rows if r["engine"] == "Gemini"]
        self.assertEqual(len(gem), 4)
        self.assertTrue(all(r["mentioned"] == "y" and r["cited"] == "y" and r["method"] == "api" for r in gem))


if __name__ == "__main__":
    unittest.main()

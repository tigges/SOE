#!/usr/bin/env python3
import os, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml

import soe_add_site as add


class AddSite(unittest.TestCase):
    def test_slug_from_host(self):
        self.assertEqual(add.slugify("Example Co", "https://www.example.com"), "example")
        self.assertEqual(add.slugify("DJ UrbanT", "https://djurbant.com"), "djurbant")
        self.assertEqual(add.slugify("Yuzu", "https://www.yuzuhairandbeauty.london", "yuzu"), "yuzu")

    def test_slug_rejects_bad(self):
        with self.assertRaises(ValueError):
            add.slugify("!", "https://www.example.com", "9bad")
        with self.assertRaises(ValueError):
            add.slugify("Nope", "https://www.example.com", "---")

    def test_url_normalise(self):
        self.assertEqual(add.normalise_url("example.com/"), "https://example.com")
        self.assertEqual(add.normalise_url("https://www.Example.com"), "https://www.Example.com")
        with self.assertRaises(ValueError):
            add.normalise_url("not a url")
        with self.assertRaises(ValueError):
            add.normalise_url("ftp://example.com")

    def test_yaml_roundtrip(self):
        cfg = add.build_config(
            "O'Hara & Sons", "https://www.ohara-and-sons.example", "local_business", "wix",
            description="A salon in Ealing: cuts, colour, blow-dries.",
            keywords="hair salon Ealing, hairdresser Ealing Broadway",
            phone="020 0000 0000", postcode="W5 2TD",
        )
        text = add.render_yaml(cfg)
        loaded = yaml.safe_load(text)
        self.assertEqual(loaded["site"]["slug"], "ohara-and-sons")
        self.assertEqual(loaded["site"]["name"], "O'Hara & Sons")
        self.assertIn("hair salon Ealing", loaded["keywords"]["primary"])
        self.assertEqual(loaded["competitors"], [])
        self.assertEqual(loaded["ai"]["engines"], ["Claude", "Gemini", "Google AI Mode"])
        self.assertTrue(text.endswith("\n"))

    def test_write_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = add.build_config("Example Co", "https://www.example.com", "saas", "nextjs")
            path = add.write_site(cfg, tmp)
            self.assertTrue(os.path.isfile(path))
            self.assertTrue(os.path.isdir(os.path.join(tmp, "projects", "example")))
            self.assertTrue(os.path.isdir(os.path.join(tmp, "data", "example")))
            with self.assertRaises(FileExistsError):
                add.write_site(cfg, tmp)
            add.write_site(cfg, tmp, force=True)

    def test_cli_print(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = add.main([
                "--name", "Example Co", "--url", "https://www.example.com",
                "--type", "generic", "--platform", "other", "--print",
            ])
        self.assertEqual(rc, 0)
        self.assertIn("slug: example", buf.getvalue())
        yaml.safe_load(buf.getvalue())

    def test_cli_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "configs"))
            with open(os.path.join(tmp, "configs", "example.yaml"), "w") as f:
                f.write("site: {slug: example}\n")
            rc = add.main([
                "--name", "Example Co", "--url", "https://www.example.com",
                "--type", "generic", "--platform", "other", "--root", tmp,
            ])
            self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()

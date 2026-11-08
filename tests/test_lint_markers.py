import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.lint_markers import ROOT, check_file


class MarkerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "raw").mkdir()
        for name in ("one.md", "two.pdf"):
            (self.root / "raw" / name).touch()
        self.page = self.root / "page.md"

    def check(self, content):
        self.page.write_text(content, encoding="utf-8")
        return check_file(self.page, self.root)

    def test_valid_markers_and_unrelated_markdown(self):
        self.assertEqual(self.check(
            "€10 [direct, source: raw/one.md]\n"
            "[synthesis, from: raw/one.md, raw/two.pdf]\n"
            "[assessment] [unverified] [directly related](other.md) [[Company]]"
        ), [])

    def test_malformed_markers(self):
        for marker in ("[Direct, source: raw/one.md]", "[synthesis from: raw/one.md]",
                       "[direct, source: ]", "[assessment: maybe]", "[unverified",
                       "[direct, source: raw/one.md"):
            with self.subTest(marker=marker):
                self.assertEqual(self.check(f"Heading\n{marker}"), [
                    (2, f"malformed marker: {marker}"),
                ])

    def test_missing_file_and_directory(self):
        for reference in ("raw/missing.pdf", "raw/directory"):
            with self.subTest(reference=reference):
                (self.root / "raw/directory").mkdir(exist_ok=True)
                self.assertIn("existing file under raw/", self.check(
                    f"[direct, source: {reference}]"
                )[0][1])

    def test_invalid_source_paths(self):
        for reference in ("wiki/page.md", "raw/../page.md", "raw//one.md",
                          "https://example.com/a", r"raw/a\b.md", "C:/raw/one.md"):
            with self.subTest(reference=reference):
                self.assertIn("invalid source path", self.check(
                    f"[direct, source: {reference}]"
                )[0][1])

    def test_reference_lists(self):
        self.assertIn("exactly one source", self.check(
            "[direct, source: raw/one.md, raw/two.pdf]"
        )[0][1])
        self.assertIn("invalid source path", self.check(
            "[synthesis, from: raw/one.md,,raw/two.pdf]"
        )[0][1])

    def test_cli_reports_file_and_line_and_exits_nonzero(self):
        self.page.write_text("Example\n[Assessment]\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/lint_markers.py"), str(self.page)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"{self.page}:2: malformed marker: [Assessment]", result.stdout)


if __name__ == "__main__":
    unittest.main()

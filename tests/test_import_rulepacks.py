import importlib.util
import io
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/image-prompt-studio/scripts/import_rulepacks.py"
SPEC = importlib.util.spec_from_file_location("import_rulepacks", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def archive_with(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return buffer.getvalue()


class RulepackImportTests(unittest.TestCase):
    def test_complete_upstream_files_and_license_are_preserved(self):
        payload = archive_with({
            "repo-sha/SKILL.md": "---\nname: upstream\ndescription: Original rules\n---\nBody",
            "repo-sha/LICENSE": "Original license",
            "repo-sha/references/details.md": "Original details",
        })
        urls = []

        def fetch(url):
            urls.append(url)
            return payload

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertTrue(MODULE.import_pack("M2", root, fetch))
            target = root / "rulepacks/moss-community"
            self.assertEqual((target / "LICENSE").read_text(), "Original license")
            self.assertEqual((target / "references/details.md").read_text(), "Original details")
            self.assertIn(MODULE.PACKS["M2"]["ref"], urls[0])
            self.assertEqual(list((root / "rulepacks").glob(".import-*")), [])

    def test_existing_rulepack_is_not_downloaded_or_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "rulepacks/krea2-prompt-suite"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("Reviewed local edits")
            self.assertFalse(MODULE.import_pack("K2", root, lambda _: self.fail("unexpected fetch")))
            self.assertEqual((target / "SKILL.md").read_text(), "Reviewed local edits")

    def test_invalid_destination_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "rulepacks/anima-prompt-crafter"
            target.mkdir(parents=True)
            (target / "notes.txt").write_text("Keep this")
            with self.assertRaises(ValueError):
                MODULE.import_pack("A1", root, lambda _: self.fail("unexpected fetch"))
            self.assertEqual((target / "notes.txt").read_text(), "Keep this")

    def test_path_traversal_leaves_no_partial_import(self):
        payload = archive_with({"repo-sha/SKILL.md": "---", "../escape.txt": "bad"})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(ValueError):
                MODULE.import_pack("M2", root, lambda _: payload)
            self.assertEqual(list((root / "rulepacks").iterdir()), [])
            self.assertFalse((root / "escape.txt").exists())

    def test_symbolic_link_archive_is_rejected(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            entry = zipfile.ZipInfo("repo-sha/link")
            entry.create_system = 3
            entry.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(entry, "../../elsewhere")
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                MODULE.extract_archive(buffer.getvalue(), Path(temporary))
            self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_missing_skill_is_not_promoted(self):
        payload = archive_with({"repo-sha/README.md": "No skill here"})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(ValueError):
                MODULE.import_pack("A1", root, lambda _: payload)
            self.assertEqual(list((root / "rulepacks").iterdir()), [])

    def test_download_failure_leaves_no_partial_import(self):
        def fail(_):
            raise OSError("network unavailable")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(OSError):
                MODULE.import_pack("K2", root, fail)
            self.assertEqual(list((root / "rulepacks").iterdir()), [])


if __name__ == "__main__":
    unittest.main()

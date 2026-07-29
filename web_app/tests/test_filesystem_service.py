import json
import tempfile
import unittest
from pathlib import Path

from web_app.config import WebAppConfig
from web_app.services.filesystem_service import FileSystemService


class FileSystemServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        root = Path(self.temporary_directory.name)
        self.config = WebAppConfig(repo_root=root, data_dir=root / "web_data")
        self.service = FileSystemService(self.config)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_reads_structured_prompt_identifier_with_dot(self) -> None:
        prompt_path = self.config.prompts_dir / "contact.structured_context.prompt.md"
        prompt_path.write_text("prompt estruturado", encoding="utf-8")

        self.assertEqual(
            self.service.read_prompt("contact.structured_context"),
            "prompt estruturado",
        )
        self.assertEqual(
            self.service.prompt_paths(["contact.structured_context"]),
            [prompt_path],
        )

    def test_lists_only_structured_context_prompts(self) -> None:
        structured = self.config.prompts_dir / "contact.structured_context.prompt.md"
        structured.write_text("estruturado", encoding="utf-8")
        (self.config.prompts_dir / "contact.baseline.prompt.md").write_text("baseline", encoding="utf-8")

        self.assertEqual(self.service.list_prompts(), [structured])

    def test_reads_crawl_manifest(self) -> None:
        self.config.crawl_manifest_path.parent.mkdir(parents=True)
        self.config.crawl_manifest_path.write_text(
            json.dumps({"target_url": "https://example.test", "random_order": False}),
            encoding="utf-8",
        )

        manifest = self.service.read_crawl_manifest()

        self.assertEqual(manifest["target_url"], "https://example.test")
        self.assertFalse(manifest["random_order"])

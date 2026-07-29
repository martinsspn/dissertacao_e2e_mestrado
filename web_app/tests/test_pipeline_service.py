import tempfile
import unittest
from pathlib import Path

from web_app.config import WebAppConfig
from web_app.services.pipeline_service import PipelineService


class _Jobs:
    def __init__(self) -> None:
        self.command: list[str] = []

    def start(self, kind, command, env=None):
        self.command = command
        return {"kind": kind, "env": env}


class PipelineServiceTest(unittest.TestCase):
    def test_auxiliary_evaluation_uses_separate_module_and_markdown_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = WebAppConfig(repo_root=root, data_dir=root / "web_data")
            jobs = _Jobs()
            service = PipelineService(config, jobs)

            service.evaluate_tests("structured_context", use_graph=False, target_url="https://example.test/")

        prompt_dir_index = jobs.command.index("--prompt-dir") + 1
        self.assertEqual(jobs.command[prompt_dir_index], str(config.prompts_dir))
        base_url_index = jobs.command.index("--base-url") + 1
        self.assertEqual(jobs.command[base_url_index], "https://example.test/")
        output_index = jobs.command.index("--output") + 1
        self.assertEqual(jobs.command[output_index], str(config.evaluation_reports_dir / "structured_context.md"))
        self.assertEqual(jobs.command[0:3], [__import__("sys").executable, "-m", "avaliacao_prompts"])

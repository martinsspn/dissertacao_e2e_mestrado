from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


Approach = Literal["baseline", "semantic_prompt"]
ExecutionStatus = Literal[
    "not_run",
    "passed",
    "failed",
    "timed_out",
    "syntax_error",
    "runtime_error",
    "environment_error",
]
FailureClassification = Literal[
    "application_failure",
    "generated_test_failure",
    "environment_failure",
    "inconclusive",
]
SelectorRisk = Literal["none", "low", "medium", "high"]


@dataclass(frozen=True)
class EvaluationCase:
    spec_id: str
    approach: Approach
    test_file: Path
    base_url: str
    prompt_file: Path | None = None


@dataclass(frozen=True)
class StaticAnalysisResult:
    has_playwright_import: bool
    has_test_block: bool
    has_expect_assertion: bool
    uses_wait_for_timeout: bool
    goto_urls: list[str] = field(default_factory=list)
    locator_texts: list[str] = field(default_factory=list)
    locator_count: int = 0
    semantic_locator_count: int = 0
    xpath_count: int = 0
    action_count: int = 0
    selector_risk: SelectorRisk = "none"


@dataclass(frozen=True)
class GraphConformanceResult:
    graph_url_coverage: float
    unknown_urls: list[str] = field(default_factory=list)
    locator_text_coverage: float = 0.0
    unknown_locator_texts: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ExecutionResult:
    status: ExecutionStatus = "not_run"
    error_type: str = ""
    error_message_excerpt: str = ""
    duration_seconds: float | None = None


@dataclass(frozen=True)
class HumanReview:
    flow_correctness: int | None = None
    target_correctness: int | None = None
    assertion_correctness: int | None = None
    graph_adherence: int | None = None
    practical_robustness: int | None = None
    overall_usefulness: int | None = None
    failure_classification: FailureClassification | None = None
    notes: str = ""


@dataclass(frozen=True)
class EvaluationReport:
    case: EvaluationCase
    static_analysis: StaticAnalysisResult
    graph_conformance: GraphConformanceResult | None = None
    execution: ExecutionResult = field(default_factory=ExecutionResult)
    human_review: HumanReview = field(default_factory=HumanReview)

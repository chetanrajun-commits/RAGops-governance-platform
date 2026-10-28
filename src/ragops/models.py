"""Domain models for the RAGOps pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    content: str
    allowed_roles: list[str]


@dataclass
class RetrievalResult:
    documents: list[Document]
    blocked_count: int = 0


@dataclass
class JudgeEvaluation:
    score: float
    passed: bool
    reason: str


@dataclass
class AuditLog:
    user_role: str
    query: str
    retrieved_doc_ids: list[str]
    blocked_doc_count: int
    generated_answer: str
    judge_evaluation: JudgeEvaluation


@dataclass
class PipelineResult:
    status: str  # "success" | "blocked"
    answer: str
    audit: AuditLog
    artifacts: dict[str, Any] = field(default_factory=dict)

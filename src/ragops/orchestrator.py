"""Orchestrator.

Wires the Retriever, Generator, and Judge into a single governed RAG pipeline.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .generator import Generator
from .judge import Judge
from .models import AuditLog
from .retriever import RBACRetriever


class Orchestrator:
    def __init__(self, docs_path: Path, config_path: Path) -> None:
        self.config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        self.retriever = RBACRetriever(
            docs_path, 
            min_score=self.config.get("min_relevance_score", 0.1)
        )
        self.generator = Generator()
        self.judge = Judge()

    def run(self, query: str, role: str) -> int:
        print(f"\n[ORCHESTRATOR] Query: '{query}' | Role: '{role}'")

        # 1. Retrieve (RBAC enforced)
        max_chunks = self.config.get("max_chunks", 2)
        retrieval_result = self.retriever.retrieve(query, role, max_chunks)
        
        print(f"[RETRIEVER]    Found {len(retrieval_result.documents)} authorized doc(s).")
        if retrieval_result.blocked_count > 0:
            print(f"[RETRIEVER]    🛑 Blocked {retrieval_result.blocked_count} unauthorized doc(s).")

        # 2. Generate
        answer = self.generator.generate(query, retrieval_result.documents)
        print(f"[GENERATOR]    Output: {answer[:80]}...")

        # 3. Judge
        evaluation = self.judge.evaluate(query, answer, retrieval_result.documents)
        print(f"[JUDGE]        Score: {evaluation.score} | Passed: {evaluation.passed}")
        print(f"[JUDGE]        Reason: {evaluation.reason}")

               # 4. Audit
        audit = AuditLog(
            user_role=role,
            query=query,
            retrieved_doc_ids=[d.id for d in retrieval_result.documents],
            blocked_doc_count=retrieval_result.blocked_count,
            generated_answer=answer,
            judge_evaluation=evaluation,
        )

        # Print the audit summary to prove it's being used
        print(f"[AUDIT]        Logged {len(audit.retrieved_doc_ids)} doc(s) for role '{audit.user_role}'.")

        if evaluation.passed:
            print("[ORCHESTRATOR] ✅ Request completed safely.")
            return 0
        else:
            print("[ORCHESTRATOR] ❌ Request blocked by Judge.")
            return 1

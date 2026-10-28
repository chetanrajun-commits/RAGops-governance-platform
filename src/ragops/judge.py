"""LLM-as-a-Judge.

Simulates a secondary LLM evaluation to ensure the generated response is:
1. Grounded in the retrieved context (no hallucinations).
2. Compliant (no toxic or unauthorized data leakage).
"""

from __future__ import annotations

from .models import Document, JudgeEvaluation


class Judge:
    def evaluate(self, query: str, answer: str, documents: list[Document]) -> JudgeEvaluation:
        # Rule 1: Check for hallucination/refusal
        if not documents:
            if "I do not have enough authorized information" in answer:
                return JudgeEvaluation(
                    score=1.0,
                    passed=True,
                    reason="Model correctly refused to answer due to lack of context."
                )
            return JudgeEvaluation(
                score=0.0,
                passed=False,
                reason="Model hallucinated an answer without any context."
            )

        # Rule 2: Ensure the answer actually uses the context
        # (Simulating a groundedness check)
        first_doc_content = documents[0].content
        if first_doc_content not in answer:
            return JudgeEvaluation(
                score=0.5,
                passed=False,
                reason="Answer does not appear to be grounded in the retrieved context."
            )

        # Rule 3: Compliance / Toxicity check (simulated)
        banned_phrases = ["social security number", "password"]
        for phrase in banned_phrases:
            if phrase in answer.lower():
                return JudgeEvaluation(
                    score=0.0,
                    passed=False,
                    reason=f"Compliance violation: output contained banned phrase '{phrase}'."
                )

        return JudgeEvaluation(
            score=0.95,
            passed=True,
            reason="Answer is grounded, compliant, and directly addresses the query."
        )

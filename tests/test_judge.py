"""Tests for the LLM-as-a-Judge."""

from __future__ import annotations

from ragops.judge import Judge
from ragops.models import Document


def test_judge_passes_grounded_answer() -> None:
    judge = Judge()
    docs = [Document(id="1", title="T", content="The policy is 3 months.", allowed_roles=["hr"])]
    answer = "Based on the retrieved documents: The policy is 3 months."
    
    result = judge.evaluate("What is the policy?", answer, docs)
    
    assert result.passed is True
    assert result.score > 0.9


def test_judge_fails_hallucination() -> None:
    judge = Judge()
    # No docs were found, but the LLM hallucinated an answer
    answer = "The policy is 6 months."
    
    result = judge.evaluate("What is the policy?", answer, documents=[])
    
    assert result.passed is False
    assert "hallucinated" in result.reason


def test_judge_passes_safe_refusal() -> None:
    judge = Judge()
    # No docs found, and the LLM correctly refused to answer
    answer = "I do not have enough authorized information to answer this question."
    
    result = judge.evaluate("What is the policy?", answer, documents=[])
    
    assert result.passed is True
    assert "correctly refused" in result.reason

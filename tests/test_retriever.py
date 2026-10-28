"""Tests for the RBAC Pre-Retrieval filtering."""

from __future__ import annotations

from ragops.retriever import RBACRetriever


def test_hr_role_gets_restricted_doc(retriever: RBACRetriever) -> None:
    # Using a highly specific query to avoid matching unrelated docs
    result = retriever.retrieve("layoff plan", user_role="hr")
    
    assert len(result.documents) == 1
    assert result.documents[0].id == "doc-2"
    assert result.blocked_count == 0


def test_engineer_role_is_blocked_from_restricted_doc(retriever: RBACRetriever) -> None:
    result = retriever.retrieve("layoff plan", user_role="engineer")
    
    # The engineer should get 0 documents because the only matching doc is restricted
    assert len(result.documents) == 0
    assert result.blocked_count == 1


def test_public_role_gets_public_doc(retriever: RBACRetriever) -> None:
    result = retriever.retrieve("Thanksgiving holiday", user_role="public")
    
    assert len(result.documents) == 1
    assert result.documents[0].id == "doc-1"

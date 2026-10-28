"""Shared fixtures for the RAGOps test suite."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from ragops.judge import Judge
from ragops.orchestrator import Orchestrator
from ragops.retriever import RBACRetriever


@pytest.fixture
def mock_docs_path(tmp_path: Path) -> Path:
    """Writes a mock docs JSON file and returns the path."""
    docs = [
        {
            "id": "doc-1",
            "title": "Public Info",
            "content": "The company holiday is Thanksgiving.",
            "allowed_roles": ["public", "hr", "engineer"]
        },
        {
            "id": "doc-2",
            "title": "Restricted Info",
            "content": "Q3 layoff plan is 15%.",
            "allowed_roles": ["hr"]
        }
    ]
    path = tmp_path / "docs.json"
    path.write_text(json.dumps(docs), encoding="utf-8")
    return path


@pytest.fixture
def config_path(tmp_path: Path) -> Path:
    """Writes a mock config YAML file and returns the path."""
    config = {
        "min_relevance_score": 0.1,
        "max_chunks": 2
    }
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    return path


@pytest.fixture
def retriever(mock_docs_path: Path) -> RBACRetriever:
    return RBACRetriever(mock_docs_path, min_score=0.1)

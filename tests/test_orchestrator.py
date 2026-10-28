"""End-to-end test of the governed RAG pipeline."""

from __future__ import annotations

from pathlib import Path

from ragops.orchestrator import Orchestrator


def test_pipeline_success_for_authorized_user(
    mock_docs_path: Path, config_path: Path
) -> None:
    orchestrator = Orchestrator(mock_docs_path, config_path)
    exit_code = orchestrator.run("layoff plan", role="hr")
    
    # Should exit 0 because the HR user is authorized and the Judge passes
    assert exit_code == 0


def test_pipeline_fails_safely_for_unauthorized_user(
    mock_docs_path: Path, config_path: Path
) -> None:
    orchestrator = Orchestrator(mock_docs_path, config_path)
    exit_code = orchestrator.run("layoff plan", role="engineer")
    
    # Should exit 0 because the Judge passes the refusal (no hallucination)
    assert exit_code == 0

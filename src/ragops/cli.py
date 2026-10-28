"""Command-line interface for the RAGOps Pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .orchestrator import Orchestrator


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ragops",
        description="Enterprise RAG Governance Pipeline.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ragops {__version__}",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run the governed RAG pipeline.")
    run.add_argument("--config", required=True, type=Path, help="Path to config YAML.")
    run.add_argument("--docs", default=Path("examples/mock-docs.json"), type=Path, help="Path to docs JSON.")
    run.add_argument("--query", required=True, type=str, help="The user's question.")
    run.add_argument("--role", required=True, type=str, help="The user's RBAC role.")
    
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command != "run":
        parser.print_help()
        sys.exit(2)

    if not args.config.exists() or not args.docs.exists():
        print("[ERROR] Config or docs file not found.", file=sys.stderr)
        sys.exit(2)

    orchestrator = Orchestrator(args.docs, args.config)
    sys.exit(orchestrator.run(args.query, args.role))


if __name__ == "__main__":
    main()

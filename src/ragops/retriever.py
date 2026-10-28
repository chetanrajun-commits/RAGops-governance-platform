"""RBAC Retriever.

Simulates a vector database search, but enforces strict role-based access
control BEFORE returning the chunks. This prevents the LLM from ever
seeing data the user isn't authorized to access.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import Document, RetrievalResult


class RBACRetriever:
    def __init__(self, docs_path: Path, min_score: float = 0.1) -> None:
        self.docs_path = docs_path
        self.min_score = min_score
        self.all_docs = self._load_docs()

    def _load_docs(self) -> list[Document]:
        data = json.loads(self.docs_path.read_text(encoding="utf-8"))
        return [Document(**d) for d in data]

    def retrieve(self, query: str, user_role: str, max_chunks: int = 2) -> RetrievalResult:
        """Retrieves matching docs, filtered strictly by the user's role."""
        query_tokens = set(query.lower().split())
        matched_docs = []
        blocked_count = 0

        for doc in self.all_docs:
            # 1. Keyword matching (simulating vector similarity)
            doc_tokens = set((doc.title + " " + doc.content).lower().split())
            overlap = len(query_tokens.intersection(doc_tokens))
            
            # Normalize score by query length
            score = overlap / max(len(query_tokens), 1)

            if score >= self.min_score:
                # 2. The RBAC Gate
                if user_role in doc.allowed_roles:
                    matched_docs.append((score, doc))
                else:
                    blocked_count += 1

        # Sort by highest score
        matched_docs.sort(key=lambda x: x[0], reverse=True)
        top_docs = [doc for _, doc in matched_docs[:max_chunks]]

        return RetrievalResult(documents=top_docs, blocked_count=blocked_count)

"""Mock LLM Generator.

Simulates the generation phase of RAG. It takes the user's query and the
retrieved, RBAC-filtered documents and synthesizes an answer.
"""

from __future__ import annotations

from .models import Document


class Generator:
    def generate(self, query: str, documents: list[Document]) -> str:
        if not documents:
            return (
                "I do not have enough authorized information to answer this question. "
                "Either the information does not exist or you do not have the required permissions."
            )

        # Simulate synthesizing an answer from the retrieved context
        context = " ".join([doc.content for doc in documents])
        
        # A real LLM would generate a cohesive paragraph. Here we simulate it.
        return f"Based on the retrieved documents: {context}"

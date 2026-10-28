# RAGOps Governance Platform

> An enterprise RAG pipeline that enforces chunk-level RBAC (Role-Based Access Control), simulates LLM-as-a-Judge evaluations, and produces deterministic audit logs.

[![CI](https://github.com/chetanrajun-commits/ragops-governance-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/chetanrajun-commits/ragops-governance-platform/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Ruff](https://img.shields.io/badge/lint-ruff-orange.svg)](https://github.com/astral-sh/ruff)

---

## The Problem

Enterprises want to use Retrieval-Augmented Generation (RAG) on their internal data, but they are paralysed by two major risks:
1. **Data Leakage:** An intern asks a question, and the LLM retrieves and summarises the CEO's salary because there are no access controls.
2. **Hallucinations & Toxicity:** The LLM makes up a compliance rule or outputs sensitive data, and the user has no way of knowing it's wrong.

This repository is a **reference implementation** of the fix: a governed RAG pipeline that enforces security *before* the LLM sees the data, and evaluates the answer *after* the LLM generates it.

## What it does

1. **Pre-Retrieval RBAC:** The retriever checks the user's role (e.g., `hr_manager`, `engineer`, `public`) against the document's `allowed_roles` metadata. Unauthorized documents are dropped before they ever enter the context window.
2. **Deterministic Generation:** A mock LLM synthesizes an answer based *only* on the authorized chunks.
3. **LLM-as-a-Judge:** A secondary evaluation agent scores the answer for groundedness (no hallucinations) and compliance.
4. **Audit Logging:** Every transaction outputs a structured report showing exactly what was retrieved, what was blocked, and how the Judge scored the output.

---

## Demo

Because this is a deterministic CLI, you can simulate both an authorised and unauthorised user.

**Test 1: Authorised User (HR Manager)**
```bash
ragops run --config examples/rbac-config.yaml --query "What is the Q3 layoff plan?" --role hr_manager

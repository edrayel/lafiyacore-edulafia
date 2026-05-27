# ADR-001: Monorepo Structure

## Status

Accepted

## Context

EduLafia consists of a Python/FastAPI backend and a React/TypeScript frontend. We needed a way to manage both codebases in a single repository with shared tooling.

## Decision

We use a pnpm workspace with Turborepo for task orchestration. The backend is managed with uv (Python package manager) as a workspace member.

## Consequences

- Single source of truth for all code
- Shared CI/CD pipeline
- Turborepo caching speeds up builds
- Requires understanding of both Python and Node ecosystems

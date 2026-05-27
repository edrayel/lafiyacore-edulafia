# ADR-002: Repository Pattern for Data Access

## Status

Accepted

## Context

We needed a clean separation between business logic and data access for testability and maintainability.

## Decision

Each module follows the pattern: models -> repository -> service -> api. The repository handles all database operations, the service handles business logic, and the API layer handles HTTP concerns.

## Consequences

- Easy to swap data sources (e.g., add caching layer)
- Services are testable without database
- Clear separation of concerns
- More files per module

# ADR-003: Cookie-Based Authentication

## Status

Accepted

## Context

Storing JWT tokens in localStorage is vulnerable to XSS attacks. We needed a more secure approach.

## Decision

We use httpOnly, secure, SameSite=lax cookies for JWT tokens. The backend sets cookies on login/refresh responses and clears them on logout. The frontend relies on the browser sending cookies automatically with `withCredentials: true`.

## Consequences

- XSS cannot access tokens
- CSRF protection via SameSite=lax
- Requires CORS with credentials enabled
- Token refresh handled transparently via API interceptor

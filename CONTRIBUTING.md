# Contributing to EduLafia

## Development Setup

1. Install dependencies:

   ```bash
   pnpm install
   cd apps/backend && uv sync && cd ../..
   ```

2. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

3. Start infrastructure:

   ```bash
   docker compose up -d
   ```

4. Run development servers:
   ```bash
   pnpm dev
   ```

## Code Standards

- Python: Ruff for linting and formatting
- TypeScript: ESLint + Prettier
- All code must pass type checking

## Testing

```bash
# Run all tests
pnpm test

# Backend tests
pnpm test:backend

# Frontend tests
pnpm test:frontend

# E2E tests
pnpm test:e2e
```

## Pull Request Process

1. Create a feature branch from `develop`
2. Write tests for new functionality
3. Ensure all CI checks pass
4. Request review from team members
5. Squash merge into `develop`

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

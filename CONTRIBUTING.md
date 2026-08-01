# Contributing to Lumio

Thanks for your interest in contributing to Lumio! This document covers everything you need to make your first (or fiftieth) contribution.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## Ways to Contribute

- **Code** — features, bug fixes, performance, tests
- **Smart contracts** — Soroban contract implementation, auditing, gas optimization
- **Docs** — fixing typos, writing guides, improving API references
- **Design** — UI/UX, the `packages/ui` design system, Figma files
- **Translation** — localizing the dashboard and docs
- **Triage** — reproducing bugs, labeling issues, answering questions in Discussions

You don't need permission to contribute — just open an issue or PR. For anything large (new modules, contract redesigns, breaking API changes), please open a [Discussion](https://github.com/lumio-network/lumio/discussions) or a design doc issue first so we can align before you invest time.

## Development Setup

### Prerequisites

- Node.js 20+ and [pnpm](https://pnpm.io) 9+ (`corepack enable`)
- Docker & Docker Compose
- Rust (stable) + [`stellar-cli`](https://developers.stellar.org/docs/tools/cli/stellar-cli) for contract work
- PostgreSQL 15+ (or use the provided `docker-compose.dev.yml`)

### Setup

```bash
git clone https://github.com/lumio-network/lumio.git
cd lumio
pnpm install
docker compose -f docker/docker-compose.dev.yml up -d
pnpm --filter api prisma:migrate
cp apps/api/.env.example apps/api/.env
pnpm dev
```

### Working on contracts

```bash
cd contracts
cargo test
cargo build --target wasm32v1-none --release
```

See [`contracts/README.md`](./contracts/README.md) for deployment to Futurenet/Testnet.

## Branching & Commits

- Branch from `main`: `feat/<short-description>`, `fix/<short-description>`, `docs/<short-description>`.
- We use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `ci:`. Commit messages are linted via commitlint + Husky.
- Keep PRs focused. Prefer several small PRs over one large PR.

## Pull Request Process

1. Fork the repo (external contributors) or branch directly (maintainers).
2. Make your changes with tests and docs updated as needed.
3. Run `pnpm lint`, `pnpm test`, and `pnpm build` locally.
4. Open a PR against `main` using the PR template — link the issue it closes with `Closes #123`.
5. A maintainer will review within a few business days. CI (lint, test, build, CodeQL) must pass before merge.
6. We use squash merges; your PR title becomes the commit message, so keep it descriptive and Conventional-Commit-formatted.

## Issue Labels

| Label | Meaning |
|---|---|
| `good first issue` | Small, well-scoped, good entry point |
| `help wanted` | Maintainers want community help |
| `bug` | Confirmed defect |
| `enhancement` | New feature or improvement |
| `documentation` | Docs-only change |
| `security` | Security-relevant, may need private disclosure first |
| `blockchain` | Soroban contracts / Stellar integration |
| `frontend` | `apps/dashboard`, `apps/admin`, `packages/ui` |
| `backend` | `apps/api` |
| `needs-design` | Needs UX/UI input before implementation |

## Style Guides

- TypeScript/JS: ESLint + Prettier, enforced via `lint-staged` on commit.
- Rust: `rustfmt` + `clippy`, enforced in CI.
- Prefer explicit types at public API boundaries; avoid `any`.

## Release Process

Lumio uses [Release Please](https://github.com/googleapis/release-please) driven by Conventional Commits to automate `CHANGELOG.md` generation and version bumps. See [`docs/release-process.md`](./docs/release-process.md).

## Getting Help

Open a [Discussion](https://github.com/lumio-network/lumio/discussions) or comment on the relevant issue. Please don't DM maintainers directly for support requests — keeping discussion public helps future contributors.

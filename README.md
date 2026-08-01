<div align="center">

# Lumio

**The Open Financial Operating System for Cooperatives**

[![CI](https://img.shields.io/github/actions/workflow/status/lumio-network/lumio/ci.yml?branch=main&label=CI)](https://github.com/lumio-network/lumio/actions/workflows/ci.yml)
[![CodeQL](https://img.shields.io/github/actions/workflow/status/lumio-network/lumio/codeql.yml?branch=main&label=CodeQL)](https://github.com/lumio-network/lumio/actions/workflows/codeql.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](./LICENSE)
[![Stellar](https://img.shields.io/badge/built%20on-Stellar%20%2F%20Soroban-7D00FF)](https://stellar.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![Discord](https://img.shields.io/badge/chat-discord-5865F2)](#community)
[![Good First Issues](https://img.shields.io/github/issues/lumio-network/lumio/good%20first%20issue)](https://github.com/lumio-network/lumio/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)

[Website](#) · [Docs](./docs) · [Roadmap](./ROADMAP.md) · [Contributing](./CONTRIBUTING.md) · [Discussions](https://github.com/lumio-network/lumio/discussions)

</div>

---

## What is Lumio?

Across Africa and many emerging markets, cooperatives, savings groups (VSLAs, ROSCAs/tontines), churches, alumni networks, and community investment clubs still manage member money through WhatsApp threads, paper ledgers, and spreadsheets. That means fraud risk, lost records, no audit trail, manual dividend math, and slow loan approvals.

**Lumio** is an open-source cooperative finance platform that pairs a modern web application with the Stellar network, so that group treasuries, savings cycles, loans, and dividends are transparent, auditable, and programmable — without requiring members to understand blockchain.

> **Status:** Pre-alpha / active design phase. Interfaces, contract APIs, and schemas below are expected to change. See [ROADMAP.md](./ROADMAP.md) for what's stable vs. exploratory.

## Why Stellar & Soroban

- **Low transaction costs** — fees measured in fractions of a cent, viable for micro-contributions typical of savings groups.
- **Fast settlement** — 3-5 second finality suits real-time treasury visibility.
- **Native multi-sig & path payments** — first-class primitives for group-controlled treasuries.
- **Soroban smart contracts** — programmable dividend distribution, governance/voting, and escrow logic that doesn't require trusting a single administrator.
- **Stellar Anchors / stablecoins** — a path to on/off-ramps in local currency without Lumio needing to become a money transmitter itself.

## Core Modules

| Module | Description |
|---|---|
| **Organization Management** | Orgs, branches, committees, member roles & permissions |
| **Group Wallets** | Multisig treasury wallets, Stellar assets & stablecoins, deposits/withdrawals |
| **Savings** | Contribution cycles, recurring savings, penalties, reminders |
| **Loans** | Requests, guarantors, approvals, repayment schedules, interest, overdue tracking |
| **Dividends** | Soroban-contract-driven, auditable profit distribution |
| **Governance** | On-chain proposals, voting, quorum, treasury approvals |
| **Treasury Dashboard** | Balances, inflows/outflows, reserves, expenses |
| **Reporting** | Monthly/annual reports, PDF/Excel export, audit reports |
| **Notifications** | Email, SMS, push, in-app |
| **Analytics** | Growth, member activity, loans, treasury, contributions |

## Monorepo Layout

```
lumio/
├─ apps/
│  ├─ dashboard/       # Next.js member & admin web app
│  ├─ admin/           # Internal/back-office console
│  ├─ documentation/   # Docs site
│  └─ api/             # NestJS backend API
├─ packages/
│  ├─ ui/              # Shared design system (shadcn/ui based)
│  ├─ sdk/              # TypeScript SDK for the Lumio API + Stellar/Soroban
│  ├─ shared/           # Cross-app types, constants, validation schemas
│  ├─ types/            # Generated/shared TypeScript types
│  └─ utilities/        # Framework-agnostic helpers
├─ contracts/           # Soroban smart contracts (Rust)
│  ├─ treasury/
│  ├─ governance/
│  ├─ dividends/
│  └─ voting/
├─ docs/                # Architecture, ADRs, guides
├─ scripts/             # Dev, release, and CI helper scripts
├─ examples/            # Minimal end-to-end usage examples
├─ docker/              # Local dev & deployment compose files
└─ .github/             # Workflows, issue/PR templates, CODEOWNERS
```

This is a [Turborepo](https://turbo.build)-managed [pnpm](https://pnpm.io) workspace. Rust contracts are a separate Cargo workspace under `contracts/`.

## Technology Stack

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS, shadcn/ui
- **Backend:** NestJS, PostgreSQL, Prisma, Redis, BullMQ
- **Blockchain:** Stellar SDK, Soroban SDK, Rust
- **Infra:** Docker, GitHub Actions, Terraform
- **Testing:** Vitest, Playwright, Jest, `cargo test`

## Quick Start

```bash
# 1. Clone
git clone https://github.com/lumio-network/lumio.git
cd lumio

# 2. Install JS/TS dependencies (Node 20+, pnpm 9+)
corepack enable
pnpm install

# 3. Start local infra (Postgres, Redis) and run migrations
docker compose -f docker/docker-compose.dev.yml up -d
pnpm --filter api prisma:migrate

# 4. Run everything in dev mode
pnpm dev
```

For Soroban contract development (Rust + `stellar-cli` required), see [`contracts/README.md`](./contracts/README.md).

Full setup instructions, including Docker-only workflows and Stellar testnet configuration, live in [`docs/getting-started.md`](./docs/getting-started.md).

## Documentation

- [Architecture Overview](./docs/architecture.md)
- [Getting Started](./docs/getting-started.md)
- [Taking This Live on GitHub](./docs/github-setup.md)
- [Security Policy](./SECURITY.md)
- [Governance](./docs/governance.md)
- [Roadmap](./ROADMAP.md)

## Contributing

Lumio is built in the open and we welcome contributions of all sizes — code, docs, design, translations, and issue triage.

1. Read [CONTRIBUTING.md](./CONTRIBUTING.md) and the [Code of Conduct](./CODE_OF_CONDUCT.md).
2. Look for issues labeled [`good first issue`](https://github.com/lumio-network/lumio/labels/good%20first%20issue) or [`help wanted`](https://github.com/lumio-network/lumio/labels/help%20wanted).
3. Join [Discussions](https://github.com/lumio-network/lumio/discussions) to propose ideas before large PRs.

## Security

Please **do not** open public issues for security vulnerabilities. See [SECURITY.md](./SECURITY.md) for our disclosure process.

## License

Lumio is licensed under the [Apache License 2.0](./LICENSE).

## Community

- GitHub Discussions: project Q&A, proposals, RFCs
- Issues: bugs and scoped feature work
- (Discord/Telegram links to be added once the community channels are live)

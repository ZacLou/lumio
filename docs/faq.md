# Frequently Asked Questions

This page collects answers to questions that come up repeatedly in GitHub Discussions, Telegram, and contributor calls. If your question is not here, open a [Discussion](https://github.com/lumio-network/lumio/discussions) and we will add it.

---

## General

### Why a monorepo?

Lumio is a full-stack cooperative-finance platform: smart contracts, backend API, web apps, shared SDK, and design system. Keeping everything in one repository makes cross-cutting changes (e.g. a contract event shape change that also requires an SDK update and a dashboard UI tweak) atomic and reviewable in a single PR. Turborepo + pnpm workspaces give us fast, cached builds without sacrificing separation of concerns.

### Why Stellar and Soroban?

- **Low fees** — viable for micro-contributions typical of savings groups.
- **Fast settlement** — 3–5 second finality suits real-time treasury visibility.
- **Native multi-sig & path payments** — first-class primitives for group-controlled treasuries.
- **Soroban smart contracts** — programmable dividend distribution, governance, and escrow without trusting a single administrator.
- **Stellar Anchors / stablecoins** — a path to on/off-ramps in local currency without Lumio needing to become a money transmitter.

### Is Lumio safe to use with real money yet?

**No.** Lumio is currently pre-alpha / active design phase. No smart contract code that custodies real funds will be deployed to mainnet until it has passed an independent security audit. See [SECURITY.md](./SECURITY.md) and [ROADMAP.md](./ROADMAP.md) for the audit gate and supported-version policy.

### Who is Lumio for?

Cooperatives, savings groups (VSLAs, ROSCAs/tontines), churches, alumni networks, and community investment clubs — especially in emerging markets — that currently manage member money through WhatsApp threads, paper ledgers, and spreadsheets.

---

## Development

### What do I need to run Lumio locally?

- Node 20+ and pnpm 9+
- Docker (for Postgres and Redis)
- Rust + `stellar-cli` (only if you are working on Soroban contracts)

See [Getting Started](./getting-started.md) for the full setup.

### Do members need to understand blockchain?

No. Lumio is designed so that every blockchain interaction has a plain-language equivalent in the UI. Members interact with savings cycles, loans, and dividends through familiar concepts; the Stellar layer is invisible to them.

### Can I self-host Lumio?

Yes, eventually. A self-hosting guide and one-click Docker/Fly.io deploy are on the roadmap for v1.0. Today the Docker Compose files under `docker/` are intended for local development, not production deployment.

---

## Security

### How do I report a security vulnerability?

Please **do not** open a public GitHub issue. Instead:

1. Use [GitHub Security Advisories](https://github.com/lumio-network/lumio/security/advisories/new) to report privately, **or**
2. Email **security@lumio.dev** with a description, reproduction steps, and affected component.

We aim to acknowledge reports within 72 hours and provide a remediation timeline within 7 days.

### Will there be a bug bounty?

Not yet. A paid bug-bounty program is planned once the project matures and secures funding. See [ROADMAP.md](./ROADMAP.md).

### What security practices are in place for smart contracts?

Before any mainnet deployment:

- Unit and integration tests (`cargo test`) for all state transitions
- Static analysis (Scout / clippy) in CI
- Independent audit of treasury, governance, and dividend contracts
- Timelocks and multisig requirements on privileged functions
- No unaudited contract code custodies real funds

---

## Roadmap & Governance

### When will Lumio be production-ready?

The current target for a mainnet-ready v1.0 is Q4 2027, subject to contributor availability, grant funding, and the security audit gate. Track live progress on the [GitHub Project board](https://github.com/orgs/lumio-network/projects) and [milestones](https://github.com/lumio-network/lumio/milestones).

### How can I influence the roadmap?

Open a [Discussion](https://github.com/lumio-network/lumio/discussions) tagged `RFC`. Roadmap changes are reviewed in the monthly community call (schedule TBD).

### What is the license?

Apache License 2.0. See [LICENSE](../LICENSE).

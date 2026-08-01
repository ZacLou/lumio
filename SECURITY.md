# Security Policy

Lumio handles group treasury funds and, eventually, real financial value on the Stellar network. We take security seriously and appreciate responsible disclosure.

## Supported Versions

While Lumio is pre-1.0, only the `main` branch and the latest tagged release receive security fixes.

| Version | Supported |
|---|---|
| `main` | ✅ |
| Latest tagged release | ✅ |
| Older tags | ❌ |

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead:

1. Use [GitHub Security Advisories](https://github.com/lumio-network/lumio/security/advisories/new) ("Report a vulnerability") for this repository, **or**
2. Email **security@lumio.dev** (placeholder — update once a project inbox exists) with:
   - A description of the vulnerability and its potential impact
   - Steps to reproduce, or a proof-of-concept
   - Affected component (contract, API, frontend, infra)

We aim to acknowledge reports within **72 hours** and provide a remediation timeline within **7 days**.

## Scope

In scope:

- `contracts/` — Soroban smart contracts (treasury, governance, dividends, voting)
- `apps/api` — backend authentication, authorization, and data handling
- `apps/dashboard`, `apps/admin` — frontend auth flows, XSS/CSRF, sensitive data exposure
- CI/CD configuration that could lead to supply-chain compromise

Out of scope:

- Denial-of-service via resource exhaustion on self-hosted instances
- Issues requiring physical access to a user's device
- Social engineering of maintainers or contributors

## Smart Contract Security

Contracts under `contracts/` follow these practices prior to any mainnet deployment:

- Unit and integration tests (`cargo test`) for all state transitions
- Static analysis (e.g. Scout / clippy) in CI
- Independent audit before any mainnet fund-custody deployment
- Timelocks and multisig requirements on privileged contract functions
- No mainnet deployment of unaudited contract code that custodies real funds

## Disclosure Policy

We follow **coordinated disclosure**: once a fix is available and deployed (or a patched release is published), we will publish a security advisory crediting the reporter (unless they prefer to remain anonymous).

## Bug Bounty

Lumio does not currently operate a paid bug bounty program. This may change as the project matures and secures funding (see [ROADMAP.md](./ROADMAP.md)).

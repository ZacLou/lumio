# Roadmap

This roadmap is directional, not a promise — dates will shift based on contributor availability and grant funding. Track live progress on the [GitHub Project board](https://github.com/orgs/lumio-network/projects) and [milestones](https://github.com/lumio-network/lumio/milestones).

## Guiding principles

1. **Custody safety before feature breadth.** No mainnet deployment of contracts that hold real member funds until audited.
2. **Usable by non-technical treasurers.** Every blockchain interaction needs a plain-language equivalent in the UI.
3. **Works offline-first markets.** SMS notifications and low-bandwidth UI are not an afterthought.

## v0.1 — Foundations (target: Q4 2026)

Scope: repo infrastructure + a working, testnet-only vertical slice (one savings group, one contribution cycle).

- [x] Monorepo scaffold, CI/CD, contribution & security docs
- [ ] Org & member management (create org, invite, roles)
- [ ] Soroban treasury contract v0 (deposit/withdraw with multisig, Testnet only)
- [ ] Basic savings module (fixed contribution cycles, manual reminders)
- [ ] Dashboard: auth, org switcher, treasury balance view
- [ ] SDK v0: TypeScript client for API + Stellar/Soroban helpers

## v0.5 — Core Financial Loop (target: Q2 2027)

- [ ] Loan module: requests, guarantors, repayment schedules, interest calc
- [ ] Dividend distribution contract (pull-based claims, auditable on-chain)
- [ ] Notification system (email + SMS via a pluggable provider interface)
- [ ] Treasury dashboard v1: inflows/outflows, reserves, expense tracking
- [ ] Reporting: monthly PDF/Excel export
- [ ] Independent security review of treasury + dividend contracts (pre-mainnet gate)

## v1.0 — Governance & Production Readiness (target: Q4 2027)

- [ ] Governance contract: proposals, voting, quorum, treasury execution
- [ ] Mainnet deployment path (post-audit) with feature-flagged rollout
- [ ] Multi-branch / multi-committee organization support
- [ ] Full analytics suite (growth, member activity, loan performance)
- [ ] Anchor integration for local-currency on/off-ramp
- [ ] Self-hosting guide + one-click Docker/Fly.io deploy

## v2.0 — Ecosystem & Scale (target: 2028)

- [ ] Rust SDK for third-party integrations
- [ ] Public API + webhooks for external accounting tools
- [ ] Plugin architecture for country-specific compliance/reporting
- [ ] Mobile app (React Native) for low-bandwidth contexts
- [ ] Multi-language support (starting with French, Swahili, Portuguese)

## How to influence the roadmap

Open a [Discussion](https://github.com/lumio-network/lumio/discussions) tagged `RFC` for anything not yet listed here. Roadmap changes are reviewed in the (forthcoming) monthly community call.

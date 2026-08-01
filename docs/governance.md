# Project Governance

Lumio is a young open-source project. This document describes how decisions are made today and how governance is expected to evolve as the contributor base grows.

## Current model: benevolent maintainer group

- A small group of maintainers (see [CODEOWNERS](../.github/CODEOWNERS)) has merge rights and makes final calls on scope, architecture, and releases.
- Day-to-day decisions (bug triage, small features) happen via normal PR review.
- Significant decisions (new modules, breaking changes, contract redesigns, dependency additions with license implications) go through an RFC in [GitHub Discussions](https://github.com/lumio-network/lumio/discussions), open for at least 5 days before a maintainer decision.

## Becoming a maintainer

There's no fixed contribution count — maintainers are added when existing maintainers agree someone has shown sustained, trustworthy judgment across multiple PRs/reviews, typically over a few months. Reach out in Discussions if you're interested; we're happy to be explicit about what we're looking for.

## Decision-making for smart contracts specifically

Given the financial stakes, contract changes require:

1. Review from at least one maintainer in `@lumio-network/contracts-team` (see CODEOWNERS).
2. Full test coverage for new/changed state transitions.
3. For anything affecting privileged functions or fund custody: a second independent reviewer, and — before mainnet deployment — an external audit (see [SECURITY.md](../SECURITY.md)).

## Evolving toward foundation/DAO governance

As the platform matures and (hopefully) member cooperatives start relying on it for real funds, we intend to evolve governance toward:

- A steering committee with representation beyond the original founding maintainers
- On-chain governance (via the `governance` Soroban contract) for protocol-level parameters once it's audited and stable
- Transparent reporting on any grant funding received and how it was used

This is intentionally not fully specified yet — it will be shaped by an RFC once the contributor base is large enough to need it.

## Code of Conduct enforcement

Handled per [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) by the maintainer group collectively, to avoid concentrating that authority in one person.

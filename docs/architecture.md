# Architecture Overview

## System context

```
                     ┌─────────────────────────┐
                     │        Members           │
                     │  (web dashboard, SMS)     │
                     └────────────┬─────────────┘
                                  │
                     ┌────────────▼─────────────┐
                     │   apps/dashboard (Next.js)│
                     │   apps/admin (Next.js)    │
                     └────────────┬─────────────┘
                                  │ REST/GraphQL
                     ┌────────────▼─────────────┐
                     │   apps/api (NestJS)       │
                     │  - Auth, RBAC             │
                     │  - Org/Savings/Loan logic │
                     │  - Job queue (BullMQ)     │
                     └───┬───────────────┬───────┘
                         │               │
              ┌──────────▼───┐   ┌───────▼──────────┐
              │ PostgreSQL    │   │ Stellar/Soroban   │
              │ (Prisma ORM)  │   │ RPC + Horizon     │
              └───────────────┘   └───────┬───────────┘
                                          │
                              ┌───────────▼────────────┐
                              │  Soroban Contracts       │
                              │  treasury / governance /  │
                              │  dividends / voting        │
                              └────────────────────────┘
```

## Design principles

1. **The database is the source of truth for off-chain state** (member profiles, notifications, UI preferences). **The blockchain is the source of truth for custody and money movement.** The API never represents a balance without it being reconcilable against on-chain state.
2. **No private keys touch the backend in plaintext.** Group treasury signing is multisig; member-held keys use client-side signing (wallet extension or embedded signer) wherever the action requires a member's own authorization.
3. **Contracts are modular, not monolithic.** `treasury`, `governance`, `dividends`, and `voting` are separate contracts with well-defined cross-contract calls, so each can be audited, upgraded, and reasoned about independently.
4. **Idempotent, queued side effects.** Notifications, report generation, and on-chain event reconciliation run through BullMQ jobs, not inline in request handlers.

## Component responsibilities

### `apps/api` (NestJS)

- AuthN (email/password + OTP; SSO planned) and RBAC (org-scoped roles: admin, treasurer, member, auditor)
- Domain logic for organizations, savings cycles, loans, and reporting
- Submits and monitors Soroban transactions on behalf of the org (co-signed, never unilaterally)
- Emits domain events consumed by the notification worker

### `apps/dashboard` / `apps/admin` (Next.js)

- Member-facing and internal back-office UIs
- Client-side wallet connection (Freighter or similar) for member-signed actions (votes, loan acceptance)
- Server components fetch via the API; no direct DB access from the frontend

### `packages/sdk`

- TypeScript client wrapping the API and Stellar/Soroban RPC calls
- Published independently so third parties can build on Lumio without depending on the whole monorepo

### `contracts/`

- `treasury` — multisig deposit/withdraw, spending policies
- `governance` — proposal lifecycle, voting, quorum, execution
- `dividends` — pull-based, auditable profit distribution
- `voting` — reusable voting primitives shared by governance and dividend approval flows

See [`contracts/README.md`](../contracts/README.md) for contract-level design notes.

## Data flow: a savings contribution

1. Member submits a contribution in the dashboard.
2. API validates against the group's active savings cycle and creates a pending record.
3. API builds a Soroban transaction invoking `treasury.deposit`; the member (or an authorized signer) signs client-side.
4. API submits the signed transaction, polls for confirmation, and reconciles the pending record against the on-chain event.
5. A BullMQ job sends a confirmation notification (email/SMS/push) and updates analytics aggregates.

## Why not custody funds off-chain at all?

Early versions may support an "off-chain ledger, on-chain settlement" mode for orgs not yet ready to fully custody on Stellar, but the target architecture treats the Soroban treasury contract as the actual custodian — the off-chain database mirrors it for fast reads and reporting, never the reverse. This is discussed further in [ADR-0001](./adr/0001-onchain-treasury-as-source-of-truth.md) *(to be written)*.

## Open questions

- Key management UX for non-technical treasurers (custodial fallback vs. self-custody, and how to communicate the tradeoff).
- SMS-based transaction approval flow for members without smartphones.
- Compliance posture per jurisdiction (Lumio itself does not want to become a money transmitter).

Discuss these in [GitHub Discussions](https://github.com/lumio-network/lumio/discussions).

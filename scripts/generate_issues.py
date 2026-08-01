import json

# Each issue: title, body, labels, milestone, module
# "difficulty" label (good first issue / help wanted) applied per-item.

M01 = "v0.1 — Foundations"
M05 = "v0.5 — Core Financial Loop"
M10 = "v1.0 — Governance & Production Readiness"
M20 = "v2.0 — Ecosystem & Scale"

issues = []

def add(title, body, labels, milestone):
    issues.append({
        "title": title,
        "body": body.strip(),
        "labels": labels,
        "milestone": milestone,
    })

# ---------- Organization Management ----------
add("Design org/member/role Prisma schema",
    "Define the initial Prisma schema for Organization, Member, Role, and Invite entities. "
    "Should support org-scoped roles (admin, treasurer, member, auditor) and branch/committee "
    "sub-grouping planned for v1.0 (leave a nullable branchId for forward compatibility).",
    ["backend", "enhancement"], M01)
add("Implement organization creation API endpoint",
    "POST /orgs — creates an organization, assigns the creator as admin. Validate name/slug "
    "uniqueness. Add request validation with class-validator DTOs.",
    ["backend", "good first issue"], M01)
add("Implement member invite flow (email-based)",
    "POST /orgs/:id/invites — generates a signed invite token, sends an email via the "
    "notification worker. Invite acceptance creates a Member record with a default role.",
    ["backend", "enhancement"], M01)
add("Add role-based access control (RBAC) guard for API routes",
    "NestJS guard that checks the requesting member's org-scoped role against a route's "
    "required permission. Should be declarative via a decorator, e.g. @RequireRole('treasurer').",
    ["backend", "security"], M01)
add("Org switcher UI component",
    "Dashboard header component to switch between organizations a member belongs to. "
    "Persists last-selected org in a cookie.",
    ["frontend", "good first issue"], M01)
add("Design branch & committee data model",
    "Extend the org schema to support branches (e.g. regional chapters) and committees "
    "(e.g. loan committee) with their own scoped permissions.",
    ["backend", "needs-discussion"], M10)
add("Audit log for org-level admin actions",
    "Record who changed what (role changes, member removal, settings changes) with "
    "timestamp and actor. Expose a read-only audit log view for admins.",
    ["backend", "security"], M05)
add("CSV bulk-import for existing member rosters",
    "Let a new org admin upload a CSV of existing members (name, phone, email) during "
    "onboarding instead of inviting one by one.",
    ["backend", "enhancement", "help wanted"], M05)

# ---------- Group Wallets / Treasury ----------
add("Extend treasury contract: multisig withdrawal with threshold approval",
    "Add withdraw() requiring N-of-M signer approval. Store signer set and threshold in "
    "contract storage, gated by set_signers()/set_threshold() callable only by governance.",
    ["blockchain", "enhancement"], M01)
add("Treasury contract: spending policy limits",
    "Support per-period spending caps (e.g. max withdrawal per day) enforced at the contract "
    "level, configurable by governance.",
    ["blockchain", "enhancement"], M05)
add("Wire treasury.deposit to Stellar Asset Contract token transfer",
    "Currently the treasury scaffold only records a balance; wire it to actually move a "
    "configured SAC token (e.g. USDC) using the token client interface.",
    ["blockchain", "enhancement"], M01)
add("API: build & submit signed treasury transactions",
    "Backend service that builds a Soroban transaction envelope for deposit/withdraw, returns "
    "it unsigned to the client for member signing, then submits once signed.",
    ["backend", "blockchain"], M01)
add("Reconciliation worker: on-chain events to off-chain ledger",
    "BullMQ job that polls/subscribes to Soroban contract events and reconciles them against "
    "pending off-chain records, marking them confirmed/failed.",
    ["backend", "blockchain"], M01)
add("Treasury balance widget (dashboard)",
    "Read-only widget showing current treasury balance, sourced from the API which itself "
    "reconciles against the contract.",
    ["frontend", "good first issue"], M01)
add("Freighter wallet connect flow",
    "Integrate Freighter (or compatible) wallet connection for member-signed actions "
    "(deposits, votes). Handle 'wallet not installed' gracefully with install prompt.",
    ["frontend", "blockchain", "good first issue"], M01)
add("Contract: emit structured events for deposit/withdraw",
    "Ensure treasury contract emits typed events with enough data for the reconciliation "
    "worker to avoid extra RPC calls.",
    ["blockchain", "good first issue"], M01)
add("Support multiple asset types per treasury (XLM + stablecoins)",
    "Extend treasury balance tracking to be per-asset rather than a single implicit asset.",
    ["blockchain", "enhancement"], M05)
add("Treasury contract audit prep: threat model doc",
    "Write a threat model for the treasury contract (privileged functions, trust "
    "assumptions, failure modes) ahead of the external audit gate in ROADMAP v0.5.",
    ["security", "documentation", "blockchain"], M05)

# ---------- Savings ----------
add("Savings cycle data model & API",
    "Model recurring contribution cycles (weekly/monthly, fixed amount or flexible) scoped "
    "to a group within an org.",
    ["backend", "enhancement"], M01)
add("Record a manual contribution (cash entry, non-blockchain)",
    "For groups not yet fully on-chain: let a treasurer record a contribution received "
    "off-platform, still reflected in reporting/analytics.",
    ["backend", "good first issue"], M01)
add("Contribution reminder scheduling",
    "BullMQ recurring job that checks upcoming/missed contributions and enqueues "
    "notification jobs (email/SMS) ahead of the due date.",
    ["backend", "enhancement"], M01)
add("Savings cycle creation UI",
    "Admin-facing form to configure a new contribution cycle: frequency, amount, "
    "start/end date, penalty rules.",
    ["frontend", "enhancement"], M01)
add("Member contribution history view",
    "Dashboard page showing a member's own contribution history for a given cycle, with "
    "on-time/late indicators.",
    ["frontend", "good first issue"], M01)
add("Penalty calculation for late/missed contributions",
    "Configurable penalty rules (flat fee or percentage) applied automatically when a "
    "contribution is marked late, with an admin override path.",
    ["backend", "enhancement"], M05)
add("Savings analytics: cycle completion rate",
    "Compute and expose the percentage of members who completed a cycle on time, for the "
    "analytics dashboard.",
    ["backend", "enhancement"], M05)
add("Flexible/variable contribution amounts",
    "Support cycles where members can contribute a variable amount above a minimum, "
    "rather than only fixed amounts.",
    ["backend", "enhancement", "help wanted"], M05)
add("SMS reminder provider integration (Africa's Talking or similar)",
    "Pluggable SMS provider interface plus a first concrete implementation, used by the "
    "reminder job.",
    ["backend", "enhancement", "help wanted"], M05)
add("CSV export of a cycle's contribution history",
    "Let a treasurer export a completed cycle's contributions as CSV for offline record-keeping.",
    ["backend", "good first issue"], M05)

# ---------- Loans ----------
add("Loan request data model & API",
    "Model loan requests: amount, purpose, requested term, requesting member, status "
    "(pending/approved/rejected/disbursed/repaid).",
    ["backend", "enhancement"], M05)
add("Guarantor flow: request & confirm guarantorship",
    "A borrower nominates one or more guarantors; guarantors must explicitly confirm "
    "before the loan request can move to committee review.",
    ["backend", "enhancement"], M05)
add("Loan approval workflow (committee voting)",
    "Support single-approver and committee-quorum approval modes, configurable per org.",
    ["backend", "enhancement"], M05)
add("Repayment schedule generator",
    "Given principal, interest rate, and term, generate an amortization schedule "
    "(equal installments to start; reducing-balance as a stretch goal).",
    ["backend", "enhancement"], M05)
add("Interest calculation module",
    "Implement flat-rate and reducing-balance interest calculation as pure, well-tested "
    "functions in packages/utilities.",
    ["backend", "good first issue"], M05)
add("Overdue loan tracking & flagging",
    "Scheduled job to flag installments past due, update loan status, and notify borrower "
    "+ guarantors.",
    ["backend", "enhancement"], M05)
add("Loan request UI (borrower flow)",
    "Multi-step form: amount/purpose, guarantor selection, review & submit.",
    ["frontend", "enhancement"], M05)
add("Loan committee review UI",
    "Queue view for committee members to review pending loan requests and vote/approve.",
    ["frontend", "enhancement"], M05)
add("Guarantor liability display",
    "Show a member their total outstanding guarantor exposure across all loans they've "
    "backed, so they understand their risk before confirming a new one.",
    ["frontend", "good first issue"], M05)
add("Loan repayment recording (manual + on-chain)",
    "Support recording a repayment both as a manual entry and as a reconciled on-chain "
    "treasury deposit tagged to a specific loan.",
    ["backend", "enhancement"], M05)

# ---------- Dividends ----------
add("Design dividends contract: pull-based claim model",
    "Contract design doc: how profit pools are funded, how a member's share is computed, "
    "and how claims are made (pull vs. push), favoring pull for gas/complexity reasons.",
    ["blockchain", "needs-discussion"], M05)
add("Implement dividends contract: fund pool & claim",
    "fund_pool() to add to a distribution pool, claim() for a member to withdraw their "
    "computed share. Must be re-entrancy safe and idempotent per distribution round.",
    ["blockchain", "enhancement"], M05)
add("Dividend share calculation: proportional to contributions",
    "Compute a member's dividend share proportional to their recorded contributions over "
    "a period, as the default (configurable) distribution formula.",
    ["blockchain", "enhancement"], M05)
add("Dividends contract unit tests: edge cases",
    "Test zero-balance members, rounding remainders, double-claim prevention, and "
    "claims after a member has left the org.",
    ["blockchain", "good first issue"], M05)
add("Dividend distribution history UI",
    "Member-facing view of past dividend distributions and their claim status.",
    ["frontend", "enhancement"], M05)
add("Admin flow: initiate a dividend distribution round",
    "Treasurer/admin UI to configure and trigger a new distribution round, with a "
    "confirmation step showing computed per-member shares before execution.",
    ["frontend", "backend", "enhancement"], M05)
add("Dividend rounding remainder handling",
    "Decide and implement a policy for leftover remainder from integer division "
    "(e.g. carry to next round vs. send to treasury reserve).",
    ["blockchain", "needs-discussion"], M05)
add("Dividends contract audit prep",
    "Threat model + test coverage report ahead of the v0.5 external audit gate.",
    ["security", "blockchain", "documentation"], M05)

# ---------- Governance ----------
add("Design governance contract: proposal lifecycle",
    "Design doc for proposal states (draft/active/passed/rejected/executed/expired), "
    "voting window, and quorum calculation.",
    ["blockchain", "needs-discussion"], M10)
add("Implement governance contract: create & vote on proposals",
    "propose(), vote(), and tally logic with configurable quorum and voting period.",
    ["blockchain", "enhancement"], M10)
add("Governance contract: execute approved treasury actions",
    "Cross-contract call from governance to treasury to execute an approved spending "
    "proposal once quorum + approval threshold are met.",
    ["blockchain", "enhancement"], M10)
add("Voting power model: one-member-one-vote vs. contribution-weighted",
    "RFC + implementation for how voting power is computed; needs a Discussion before "
    "implementation given the tradeoffs.",
    ["blockchain", "needs-discussion"], M10)
add("Proposal creation & voting UI",
    "Member-facing UI to browse active proposals, view details, and cast a vote "
    "(wallet-signed).",
    ["frontend", "enhancement"], M10)
add("Governance contract: timelock for contract upgrades",
    "Require a timelock delay between a governance-approved upgrade and its execution, "
    "so members have time to react.",
    ["blockchain", "security"], M10)
add("Quorum edge case tests: low-participation proposals",
    "Test behavior when turnout is below quorum at the voting deadline (should expire, "
    "not silently pass).",
    ["blockchain", "good first issue"], M10)
add("Governance contract audit prep",
    "Threat model + test coverage ahead of the v1.0 audit gate.",
    ["security", "blockchain", "documentation"], M10)

# ---------- Treasury Dashboard ----------
add("Treasury dashboard: inflows/outflows chart",
    "Time-series chart of treasury inflows vs. outflows over a selectable period.",
    ["frontend", "enhancement"], M05)
add("Treasury dashboard: reserves indicator",
    "Show current reserve level against a configured target reserve, with a visual "
    "warning state when below target.",
    ["frontend", "good first issue"], M05)
add("Expense recording & categorization",
    "Let a treasurer record non-loan, non-dividend expenses with categories, for "
    "accurate treasury dashboard reporting.",
    ["backend", "enhancement"], M05)
add("Treasury dashboard: transaction drill-down",
    "Click into a treasury dashboard chart point to see the underlying transactions.",
    ["frontend", "enhancement"], M05)
add("Investment tracking (external to on-chain treasury)",
    "Track group investments held outside the Stellar treasury (e.g. land, equipment) "
    "for a complete net-worth picture in reporting.",
    ["backend", "enhancement", "help wanted"], M10)
add("Treasury dashboard: mobile-responsive layout pass",
    "Audit and fix the treasury dashboard for small-screen usability.",
    ["frontend", "good first issue"], M05)

# ---------- Reporting ----------
add("Monthly report generation (PDF)",
    "Scheduled job that generates a monthly org financial summary as PDF (contributions, "
    "loans, treasury balance) and stores it for download.",
    ["backend", "enhancement"], M05)
add("Excel export for contribution/loan data",
    "Add .xlsx export alongside PDF for members who want to work with the data further.",
    ["backend", "good first issue"], M05)
add("Annual report template",
    "Design and implement a yearly summary report layout, distinct from the monthly one.",
    ["backend", "design", "enhancement"], M05)
add("Audit report: full transaction trail export",
    "Export every recorded transaction (on-chain + manual) for a given period, formatted "
    "for external auditor review.",
    ["backend", "enhancement"], M05)
add("Report generation queue & retry handling",
    "Ensure report generation jobs (which can be slow for large orgs) are queued, retried "
    "on failure, and don't block API request threads.",
    ["backend", "infra"], M05)
add("Report download UI & history",
    "Dashboard page listing previously generated reports with download links.",
    ["frontend", "good first issue"], M05)
add("Localized report templates (starting with currency formatting)",
    "Support locale-aware number/currency formatting in generated reports as a first "
    "step toward full i18n in v2.0.",
    ["backend", "enhancement", "help wanted"], M20)

# ---------- Notifications ----------
add("Notification provider abstraction (email/SMS/push)",
    "Define a common interface so email, SMS, and push providers can be swapped without "
    "touching call sites.",
    ["backend", "enhancement"], M01)
add("Email notification provider (SMTP/transactional email service)",
    "First concrete implementation of the notification provider interface.",
    ["backend", "good first issue"], M01)
add("In-app notification center",
    "Bell icon + dropdown showing recent in-app notifications, with read/unread state.",
    ["frontend", "enhancement"], M05)
add("Notification preferences per member",
    "Let members opt in/out of specific notification types and channels.",
    ["backend", "frontend", "enhancement"], M05)
add("Push notification provider (web push)",
    "Implement web push as another notification provider, gated behind user opt-in.",
    ["backend", "enhancement", "help wanted"], M10)
add("Notification templates system",
    "Centralize notification copy as templates with variable interpolation, so wording "
    "changes don't require code changes.",
    ["backend", "good first issue"], M05)
add("Digest notifications (daily/weekly summary)",
    "Optional digest mode that batches non-urgent notifications instead of sending "
    "immediately.",
    ["backend", "enhancement", "help wanted"], M10)

# ---------- Analytics ----------
add("Analytics event pipeline",
    "Lightweight internal event tracking (contribution made, loan approved, vote cast) "
    "feeding into aggregate tables for the analytics dashboard.",
    ["backend", "enhancement"], M05)
add("Member activity analytics view",
    "Show org admins member engagement over time (contributions, votes, logins).",
    ["frontend", "backend", "enhancement"], M10)
add("Loan statistics dashboard",
    "Default/on-time repayment rates, average loan size, and portfolio-at-risk metrics.",
    ["frontend", "backend", "enhancement"], M10)
add("Treasury analytics: growth over time",
    "Chart treasury balance growth over time with configurable date ranges.",
    ["frontend", "good first issue"], M10)
add("Contribution analytics: cohort comparison",
    "Compare contribution consistency across different savings groups within the same org.",
    ["frontend", "backend", "enhancement", "help wanted"], M10)
add("Analytics data export API",
    "Expose the underlying analytics aggregates via API for orgs that want to build "
    "custom dashboards.",
    ["backend", "sdk", "enhancement"], M20)
add("Analytics dashboard performance: materialized views",
    "Move slow aggregate queries to materialized views refreshed on a schedule, once "
    "real usage data shows query latency issues.",
    ["backend", "infra", "help wanted"], M10)

# ---------- SDK ----------
add("SDK: TypeScript client scaffold for the API",
    "Generate/hand-write a typed client for core API endpoints (orgs, savings, loans) "
    "as the foundation of @lumio/sdk.",
    ["sdk", "enhancement"], M01)
add("SDK: Soroban transaction-building helpers",
    "Wrap common Soroban transaction construction (deposit, vote, claim dividend) behind "
    "simple SDK functions.",
    ["sdk", "blockchain", "enhancement"], M01)
add("SDK: contract event subscription helper",
    "Convenience wrapper for subscribing to/polling Soroban contract events, used by both "
    "the API reconciliation worker and third-party integrators.",
    ["sdk", "blockchain", "enhancement"], M05)
add("SDK: publish to npm as @lumio/sdk",
    "Set up the package.json, build config, and CI step to publish the SDK independently "
    "of the rest of the monorepo.",
    ["sdk", "infra"], M05)
add("SDK: usage example — create org & record a contribution",
    "A runnable example under examples/ showing the full flow end-to-end in under 30 lines.",
    ["sdk", "documentation", "good first issue"], M01)
add("SDK: React hooks package",
    "Optional @lumio/sdk-react package with hooks (useTreasuryBalance, useProposals) "
    "for consumers building on React.",
    ["sdk", "frontend", "enhancement", "help wanted"], M10)
add("SDK: error handling & typed error classes",
    "Replace generic thrown errors with typed error classes so SDK consumers can "
    "handle specific failure modes.",
    ["sdk", "good first issue"], M05)
add("SDK: Rust client for third-party integrations",
    "Rust equivalent of the TypeScript SDK, for integrators working outside the JS "
    "ecosystem.",
    ["sdk", "blockchain", "help wanted"], M20)

# ---------- Design System ----------
add("Design system: token setup (color, spacing, typography)",
    "Establish the base design tokens in packages/ui as Tailwind config + CSS variables.",
    ["design", "frontend", "good first issue"], M01)
add("Design system: Button, Input, Select primitives",
    "Core form primitives built on shadcn/ui, themed with Lumio's design tokens.",
    ["design", "frontend", "good first issue"], M01)
add("Design system: data table component",
    "Reusable sortable/filterable table used across contribution, loan, and report lists.",
    ["design", "frontend", "enhancement"], M01)
add("Design system: empty states & loading skeletons",
    "Consistent empty-state and skeleton-loading components for use across the dashboard.",
    ["design", "frontend", "good first issue"], M05)
add("Design system: Storybook setup",
    "Add Storybook to packages/ui so components can be developed and reviewed in "
    "isolation.",
    ["design", "infra", "help wanted"], M05)
add("Accessibility audit of core components",
    "Run an a11y audit (axe or similar) over packages/ui primitives and fix issues found.",
    ["design", "frontend", "help wanted"], M05)

# ---------- Documentation ----------
add("Write ADR template & first ADR (on-chain treasury as source of truth)",
    "Add docs/adr/ with a lightweight ADR template, and write ADR-0001 referenced from "
    "docs/architecture.md.",
    ["documentation", "good first issue"], M01)
add("API reference documentation (OpenAPI/Swagger)",
    "Generate and publish OpenAPI docs from the NestJS API, served at /docs.",
    ["documentation", "backend", "good first issue"], M01)
add("Contract API reference (per-contract function docs)",
    "Document each public contract function's parameters, auth requirements, and "
    "possible panics, generated from doc comments where possible.",
    ["documentation", "blockchain", "good first issue"], M01)
add("Deployment guide: self-hosting with Docker Compose",
    "Step-by-step guide for a co-op to self-host the full stack, including Stellar "
    "network configuration choices.",
    ["documentation", "infra"], M10)
add("FAQ page",
    "Collect and answer common questions from Discussions/support into a living FAQ doc.",
    ["documentation", "good first issue"], M05)
add("Troubleshooting guide",
    "Document common local-dev issues (from the Getting Started troubleshooting section) "
    "in more depth as they're reported.",
    ["documentation", "good first issue"], M01)
add("Translate README into French",
    "First localized README, targeting Francophone West African cooperative communities.",
    ["documentation", "good first issue", "help wanted"], M20)
add("Video walkthrough: local dev setup",
    "Short screen-recording walkthrough of the Getting Started guide, linked from the docs "
    "site.",
    ["documentation", "help wanted"], M05)

# ---------- Infra / CI ----------
add("Set up Playwright for e2e testing",
    "Configure Playwright against the dashboard app with a basic smoke-test suite "
    "(login, view treasury balance).",
    ["infra", "frontend", "enhancement"], M01)
add("Preview deployments for PRs",
    "Configure preview deploys (Vercel or similar) for apps/dashboard on every PR.",
    ["infra", "good first issue"], M01)
add("Terraform module: base infrastructure",
    "Terraform for the managed Postgres, Redis, and app hosting environment used in "
    "staging/production.",
    ["infra", "help wanted"], M05)
add("Add Scout static analysis to contracts CI",
    "Integrate CoinFabrik's Scout (or similar Soroban-focused static analyzer) into the "
    "contracts CI job.",
    ["infra", "blockchain", "security"], M05)
add("Docker production images",
    "Multi-stage Dockerfiles for apps/api and apps/dashboard optimized for production "
    "(not just the dev compose setup).",
    ["infra", "enhancement"], M05)
add("Add bundle-size CI check for frontend apps",
    "Fail CI (or warn) if a PR significantly increases the dashboard's JS bundle size.",
    ["infra", "frontend", "good first issue"], M05)

# ---------- Security ----------
add("Rate limiting on auth endpoints",
    "Add rate limiting (e.g. via Redis) to login/OTP endpoints to mitigate brute-force "
    "attempts.",
    ["backend", "security", "good first issue"], M01)
add("Input validation audit across API DTOs",
    "Review all NestJS DTOs for missing or weak validation (class-validator decorators), "
    "particularly on amount/financial fields.",
    ["backend", "security", "good first issue"], M01)
add("Secrets handling review",
    "Audit how secrets (JWT signing key, provider API keys) are loaded and ensure none "
    "can leak into logs or client bundles.",
    ["security", "infra"], M01)
add("Add security headers middleware",
    "Configure standard security headers (CSP, HSTS, X-Content-Type-Options, etc.) for "
    "apps/api responses.",
    ["backend", "security", "good first issue"], M01)
add("Dependency vulnerability scanning gate in CI",
    "Fail CI on newly introduced high/critical vulnerabilities from `pnpm audit` / "
    "`cargo audit`.",
    ["infra", "security"], M05)
add("Document key management options for treasurers",
    "Compare self-custody vs. custodial-fallback signing UX for non-technical treasurers, "
    "feeding the open question in docs/architecture.md.",
    ["documentation", "security", "needs-discussion"], M05)

with open("/home/claude/lumio/.github/project-management/issues.json", "w") as f:
    json.dump(issues, f, indent=2)

print(f"Generated {len(issues)} issues")

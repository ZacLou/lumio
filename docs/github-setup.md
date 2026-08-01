# Getting Lumio Live on GitHub

This is the step-by-step path from "zip file on your laptop" to "a real,
properly configured GitHub repo with CI, labels, milestones, and issues
populated." Follow it roughly in order — later steps assume earlier ones
are done.

Placeholders to replace as you go: `lumio-network` (org name), `lumio`
(repo name), any `@lumio-network/*-team` handles, and the placeholder emails
in `SECURITY.md` / `CODE_OF_CONDUCT.md`.

---

## 0. Prerequisites

- A GitHub account (and, ideally, a GitHub **organization** — `lumio-network`
  or whatever you choose — rather than a personal repo, since `CODEOWNERS`
  references team handles).
- [`gh` CLI](https://cli.github.com/) installed and authenticated:
  ```bash
  gh auth login
  ```
- `jq` and [`yq`](https://github.com/mikefarah/yq) installed (used by the
  project-management scripts):
  ```bash
  # macOS
  brew install jq yq
  # Debian/Ubuntu
  sudo apt install jq && sudo snap install yq
  ```
- Git configured locally (`git config --global user.name/user.email`).

---

## 1. Create the GitHub organization (recommended) and teams

If you don't already have one:

```bash
# Organizations can't be created via gh CLI — do this in the browser:
# https://github.com/organizations/new
```

Once the org exists, create the teams referenced in `.github/CODEOWNERS`:

```bash
gh api orgs/lumio-network/teams -f name="maintainers" -f privacy="closed"
gh api orgs/lumio-network/teams -f name="contracts-team" -f privacy="closed"
gh api orgs/lumio-network/teams -f name="backend-team" -f privacy="closed"
gh api orgs/lumio-network/teams -f name="frontend-team" -f privacy="closed"
gh api orgs/lumio-network/teams -f name="design-team" -f privacy="closed"
gh api orgs/lumio-network/teams -f name="docs-team" -f privacy="closed"
gh api orgs/lumio-network/teams -f name="security-team" -f privacy="closed"
```

Add yourself (and any co-founders) to `maintainers` at minimum. If you're
starting solo, either simplify `CODEOWNERS` to just your username or create
the teams anyway so `CODEOWNERS` doesn't reference non-existent handles
(GitHub will otherwise silently ignore that owner line).

---

## 2. Create the repository

```bash
gh repo create lumio-network/lumio \
  --public \
  --description "The Open Financial Operating System for Cooperatives" \
  --homepage "https://lumio.dev"
```

(Use `--private` initially if you'd rather build in private and flip to
public later — grant programs generally want to see history, so public from
day one is usually better if you're comfortable with that.)

---

## 3. Push the scaffold

From the unzipped `lumio/` folder:

```bash
cd lumio
git init -b main
git add .
git commit -m "chore: initial repository scaffold

Monorepo layout, CI/CD, issue & PR templates, security policy,
contribution guide, and Soroban contract scaffolding."
git remote add origin https://github.com/lumio-network/lumio.git
git push -u origin main
```

---

## 4. Repo settings

In the browser (`Settings` tab) or via `gh api`:

**General**
- Set the description/topics: `gh repo edit lumio-network/lumio --add-topic stellar --add-topic soroban --add-topic cooperative-finance --add-topic fintech --add-topic open-source`
- Default branch: `main` (already set by `git init -b main`)
- Features: enable **Issues**, **Discussions**, disable **Wiki** (docs live in `/docs`)
  ```bash
  gh repo edit lumio-network/lumio --enable-issues --enable-discussions --enable-wiki=false
  ```

**Pull Requests**
- Squash merging only (keeps history clean, matches `CONTRIBUTING.md`):
  ```bash
  gh repo edit lumio-network/lumio \
    --enable-squash-merge --enable-merge-commit=false --enable-rebase-merge=false \
    --delete-branch-on-merge
  ```

**Branch protection on `main`** — require CI + review before merge:

```bash
gh api -X PUT repos/lumio-network/lumio/branches/main/protection \
  -f required_status_checks[strict]=true \
  -f 'required_status_checks[contexts][]=Lint & Typecheck (JS/TS)' \
  -f 'required_status_checks[contexts][]=Test (Vitest/Jest)' \
  -f 'required_status_checks[contexts][]=Build all apps/packages' \
  -f 'required_status_checks[contexts][]=Soroban Contracts (fmt, clippy, test)' \
  -f enforce_admins=true \
  -f 'required_pull_request_reviews[required_approving_review_count]=1' \
  -f 'required_pull_request_reviews[require_code_owner_reviews]=true' \
  -f restrictions=null
```

If that JSON-via-flags syntax fights you, it's easier done once in the
browser: **Settings → Branches → Add rule** → protect `main`, require status
checks (pick the four CI job names above), require 1 approval, require
CODEOWNERS review, and check "Do not allow bypassing" only once you're not
the only maintainer (otherwise you'll lock yourself out of solo-merging).

---

## 5. Enable security features

```bash
# CodeQL (workflow already in .github/workflows/codeql.yml — this just
# confirms default setup isn't fighting the custom workflow)
gh api -X PATCH repos/lumio-network/lumio \
  -f security_and_analysis='{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}'
```

Dependabot alerts + security updates (Settings → Code security → enable
"Dependabot alerts" and "Dependabot security updates" — `dependabot.yml`
already handles version-update PRs, this separately enables vulnerability
alerts).

Go to **Settings → Security → Security policy** and confirm it's picking up
`SECURITY.md` automatically (it will, since it's at the repo root).

---

## 6. Populate labels, milestones, issues, and the project board

This is exactly what the scripts in `scripts/` and config in
`.github/project-management/` are for — see
[`.github/project-management/README.md`](../.github/project-management/README.md)
for details. In order:

```bash
./scripts/setup-labels.sh lumio-network/lumio
./scripts/setup-milestones.sh lumio-network/lumio
./scripts/seed-issues.sh lumio-network/lumio

# Project board (needs the `project` OAuth scope)
gh auth refresh -s project
./scripts/setup-project-board.sh lumio-network lumio
```

Sanity-check afterward:

```bash
gh issue list --repo lumio-network/lumio --label "good first issue" --limit 10
gh api repos/lumio-network/lumio/milestones --jq '.[].title'
```

---

## 7. CI secrets and integrations

`ci.yml` references `CODECOV_TOKEN` (optional — the step is
`continue-on-error: true`, so CI won't fail without it, but coverage
reporting won't work). To enable it:

1. Sign up at [codecov.io](https://codecov.io), add the repo.
2. Copy the upload token.
3. `gh secret set CODECOV_TOKEN --repo lumio-network/lumio`

`release-please.yml` and `contracts-release.yml` use the default
`GITHUB_TOKEN`, which works out of the box — no extra secrets needed unless
you later want Release Please PRs to trigger *other* workflows (the default
token intentionally doesn't re-trigger workflows, to avoid loops; if you
need that, switch to a fine-grained PAT stored as a secret).

If/when you wire up real notification providers, deployment targets, etc.,
add those as repo or environment secrets rather than committing them —
`apps/api/.env.example` documents which variables exist.

---

## 8. First green CI run

Open a small PR (e.g. tweak a README typo) to confirm:

- `CI` workflow runs and all four jobs pass
- `CodeQL` runs
- Branch protection actually blocks merge until checks pass and CODEOWNERS approves

Expect the **Soroban Contracts** job to be the one most likely to need
iteration first — `soroban-sdk` version pinning and `wasm32v1-none` target
availability shift over time; check
[docs.stellar.org](https://developers.stellar.org) if it fails on a fresh
run and adjust `contracts/Cargo.toml`'s `soroban-sdk` version accordingly.

---

## 9. Community-health polish

- Add a **social preview image** (Settings → General → Social preview) — a
  simple 1280×640 image with the Lumio wordmark goes a long way for how the
  repo looks when shared.
- Pin 2–3 issues (e.g. a "Welcome, start here" discussion, the roadmap) via
  `gh issue pin`.
- Post an intro in **Discussions** (`gh api repos/lumio-network/lumio/discussions` or the web UI) — grant reviewers and early contributors both look at Discussions activity as a signal of a live project.
- Update `FUNDING.yml` once your Drips/Open Collective/OnlyDust accounts exist — placeholders are in there now and will 404 until real.

---

## 10. Applying to grant programs

Once the repo is live with real commit history (not just one big initial
commit — a few days of incremental PRs helps), you're in reasonable shape to
apply to:

- **Stellar Community Fund** — https://communityfund.stellar.org
- **OnlyDust** — https://app.onlydust.com (list the repo, they track
  contribution activity directly from GitHub)
- **Drips** — https://drips.network (funding streams tied to GitHub repos/orgs)

Each has its own application form; none of that is scriptable, but having
`README.md`, `ROADMAP.md`, `SECURITY.md`, and a populated issue tracker with
`good first issue` labels *before* you apply is exactly what reviewers check
for, and all of that's already in the scaffold.

---

## Quick reference: full sequence

```bash
gh auth login
gh repo create lumio-network/lumio --public --description "The Open Financial Operating System for Cooperatives"
cd lumio && git init -b main && git add . && git commit -m "chore: initial repository scaffold" \
  && git remote add origin https://github.com/lumio-network/lumio.git && git push -u origin main
gh repo edit lumio-network/lumio --enable-issues --enable-discussions --enable-wiki=false \
  --enable-squash-merge --enable-merge-commit=false --enable-rebase-merge=false --delete-branch-on-merge
# set branch protection (see step 4)
./scripts/setup-labels.sh lumio-network/lumio
./scripts/setup-milestones.sh lumio-network/lumio
./scripts/seed-issues.sh lumio-network/lumio
gh auth refresh -s project && ./scripts/setup-project-board.sh lumio-network lumio
```

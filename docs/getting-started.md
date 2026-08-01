# Getting Started

## Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Node.js | 20+ | Frontend/backend apps |
| pnpm | 9+ (`corepack enable`) | JS/TS package management |
| Docker + Docker Compose | latest | Postgres, Redis, local dev infra |
| Rust | stable | Soroban contracts |
| `stellar-cli` | latest | Build/deploy/invoke contracts |

## 1. Clone and install

```bash
git clone https://github.com/lumio-network/lumio.git
cd lumio
corepack enable
pnpm install
```

## 2. Start local infrastructure

```bash
docker compose -f docker/docker-compose.dev.yml up -d
```

This starts PostgreSQL and Redis with sane local defaults (see `docker/docker-compose.dev.yml`).

## 3. Configure environment variables

```bash
cp apps/api/.env.example apps/api/.env
cp apps/dashboard/.env.example apps/dashboard/.env.local
```

Key variables:

```bash
# apps/api/.env
DATABASE_URL=postgresql://lumio:lumio@localhost:5432/lumio_dev
REDIS_URL=redis://localhost:6379
STELLAR_NETWORK=TESTNET
SOROBAN_RPC_URL=https://soroban-testnet.stellar.org
JWT_SECRET=replace-me-in-dev-only
```

## 4. Run database migrations

```bash
pnpm --filter api prisma:migrate
```

## 5. Start the apps

```bash
pnpm dev
```

This runs `dashboard`, `admin`, and `api` concurrently via Turborepo. Default ports:

- Dashboard: http://localhost:3000
- Admin: http://localhost:3001
- API: http://localhost:4000 (docs at `/docs`)

## Working with Soroban contracts

```bash
cd contracts
rustup target add wasm32v1-none
cargo test
cargo build --target wasm32v1-none --release
```

Deploy to Testnet (requires `stellar-cli` configured with a funded Testnet account):

```bash
stellar contract deploy \
  --wasm target/wasm32v1-none/release/lumio_treasury.wasm \
  --source alice \
  --network testnet
```

See [`contracts/README.md`](../contracts/README.md) for per-contract instructions and [`docs/architecture.md`](./architecture.md) for how contracts fit into the wider system.

## Running tests

```bash
pnpm test          # unit tests across all JS/TS packages
pnpm test:e2e       # Playwright end-to-end tests
cd contracts && cargo test   # contract tests
```

## Troubleshooting

**`prisma:migrate` fails with connection refused** — make sure `docker compose ... up -d` finished starting Postgres (`docker compose -f docker/docker-compose.dev.yml ps`).

**`stellar-cli` can't find a funded account** — fund a Testnet account via [Friendbot](https://developers.stellar.org/docs/tools/developer-tools/friendbot).

**Port already in use** — override with `PORT=xxxx pnpm --filter dashboard dev`.

More questions? Open a [Discussion](https://github.com/lumio-network/lumio/discussions).

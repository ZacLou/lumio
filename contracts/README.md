# Lumio Soroban Contracts

Cargo workspace containing all Soroban smart contracts. Each contract is a
separate crate so it can be built, tested, audited, and upgraded independently.

| Contract | Purpose | Status |
|---|---|---|
| `treasury` | Multisig group wallet: deposits, withdrawals, spending policies | design |
| `governance` | Proposal lifecycle, voting, quorum, treasury-approval execution | design |
| `dividends` | Auditable, pull-based profit distribution to members | design |
| `voting` | Reusable voting primitives shared by governance & dividends | design |

None of these contracts are audited. **Do not deploy to Mainnet or use with
real funds.** See [SECURITY.md](../SECURITY.md).

## Build

```bash
rustup target add wasm32v1-none
cargo build --target wasm32v1-none --release
```

## Test

```bash
cargo test --all
```

## Lint

```bash
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
```

## Deploy to Testnet

```bash
stellar contract deploy \
  --wasm target/wasm32v1-none/release/lumio_treasury.wasm \
  --source <your-testnet-identity> \
  --network testnet
```

## Design notes

- **Modularity**: contracts call each other via typed cross-contract calls
  (e.g. `governance` invokes `treasury` to execute an approved spend) rather
  than sharing storage directly.
- **Upgradability**: contracts use Soroban's upgradeable-contract pattern
  behind a timelock controlled by `governance`, so no single admin key can
  silently swap contract logic.
- **No unbounded loops over user-supplied collections** in any function that
  can be called permissionlessly, to avoid resource-limit DoS.

See [`docs/architecture.md`](../docs/architecture.md) for how these contracts
fit into the broader system.

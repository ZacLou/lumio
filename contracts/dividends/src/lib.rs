//! Lumio Dividends contract (scaffold).
//!
//! Not yet implemented — placeholder crate so the workspace builds and CI
//! has something to lint/test/compile to wasm. Design notes live in
//! docs/architecture.md and ROADMAP.md. Tracked for implementation in a
//! follow-up PR (see ROADMAP v0.1/v0.5/v1.0 for scope split across
//! treasury/dividends/governance/voting).
#![no_std]

use soroban_sdk::{contract, contractimpl, Env};

#[contract]
pub struct DividendsContract;

#[contractimpl]
impl DividendsContract {
    /// Placeholder health-check entrypoint. Returns true once the contract
    /// is deployed and callable. Real dividends logic replaces this.
    pub fn ping(_env: Env) -> bool {
        true
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn ping_returns_true() {
        let env = Env::default();
        let contract_id = env.register(DividendsContract, ());
        let client = DividendsContractClient::new(&env, &contract_id);
        assert!(client.ping());
    }
}

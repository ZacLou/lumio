//! Lumio Treasury contract (scaffold).
//!
//! Design target (see docs/architecture.md and ROADMAP.md v0.1):
//! - Multisig-controlled group wallet.
//! - `deposit`: any member (or an authorized payer) can top up the treasury.
//! - `withdraw`: requires threshold approval from designated signers.
//! - `set_signers` / `set_threshold`: governance-gated (invoked by the
//!   `governance` contract, not directly by an admin key).
//!
//! This is an intentionally minimal scaffold: balance tracking and a single
//! authorized-deposit path, with withdrawal/multisig logic to follow. Do not
//! deploy to Mainnet — unaudited, no real fund custody support yet.

#![no_std]

use soroban_sdk::{contract, contractimpl, contracttype, Address, Env};

#[contracttype]
#[derive(Clone)]
pub enum DataKey {
    Balance(Address),
    TotalDeposits,
}

#[contract]
pub struct TreasuryContract;

#[contractimpl]
impl TreasuryContract {
    /// Record a deposit from `depositor` into the org treasury.
    /// Requires `depositor`'s authorization. Actual asset transfer via the
    /// Stellar Asset Contract is wired in once the token interface lands
    /// (tracked in ROADMAP v0.1).
    pub fn deposit(env: Env, depositor: Address, amount: i128) {
        depositor.require_auth();
        assert!(amount > 0, "deposit amount must be positive");

        let key = DataKey::Balance(depositor);
        let current: i128 = env.storage().persistent().get(&key).unwrap_or(0);
        env.storage().persistent().set(&key, &(current + amount));

        let total: i128 = env
            .storage()
            .instance()
            .get(&DataKey::TotalDeposits)
            .unwrap_or(0);
        env.storage()
            .instance()
            .set(&DataKey::TotalDeposits, &(total + amount));
    }

    /// Read a member's recorded contribution balance.
    pub fn balance_of(env: Env, member: Address) -> i128 {
        env.storage()
            .persistent()
            .get(&DataKey::Balance(member))
            .unwrap_or(0)
    }

    /// Read the treasury's total recorded deposits.
    pub fn total_deposits(env: Env) -> i128 {
        env.storage()
            .instance()
            .get(&DataKey::TotalDeposits)
            .unwrap_or(0)
    }
}

#[cfg(test)]
mod test {
    use super::*;
    use soroban_sdk::testutils::Address as _;

    #[test]
    fn deposit_increases_balance_and_total() {
        let env = Env::default();
        env.mock_all_auths();

        let contract_id = env.register(TreasuryContract, ());
        let client = TreasuryContractClient::new(&env, &contract_id);

        let member = Address::generate(&env);

        client.deposit(&member, &100);
        client.deposit(&member, &50);

        assert_eq!(client.balance_of(&member), 150);
        assert_eq!(client.total_deposits(), 150);
    }

    #[test]
    #[should_panic(expected = "deposit amount must be positive")]
    fn rejects_non_positive_deposit() {
        let env = Env::default();
        env.mock_all_auths();

        let contract_id = env.register(TreasuryContract, ());
        let client = TreasuryContractClient::new(&env, &contract_id);
        let member = Address::generate(&env);

        client.deposit(&member, &0);
    }
}

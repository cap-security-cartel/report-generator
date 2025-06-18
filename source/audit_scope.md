The audit was started on commit [ad1f8d7](https://github.com/cap-labs-dev/cap-contracts/tree/ad1f8d772585e3c4ba3d308f7ae72d113554978e) for **15** days and a subsequent fix review was conducted on final commit [ad1f8d7](https://github.com/cap-labs-dev/cap-contracts/tree/ad1f8d772585e3c4ba3d308f7ae72d113554978e) that went for **2** days.

The following contracts were included as part of the review scope, including any related external dependencies:
```sh
access
├── Access.sol
└── AccessControl.sol
delegation
├── Delegation.sol
└── providers
    └── symbiotic
        ├── Network.sol
        └── NetworkMiddleware.sol
feeAuction
└── FeeAuction.sol
feeReceiver
└── FeeReceiver.sol
interfaces
├── IAaveDataProvider.sol
├── IAccess.sol
├── IAccessControl.sol
├── ICapToken.sol
├── IChainlink.sol
├── IDebtToken.sol
├── IDelegation.sol
├── IFeeAuction.sol
├── IFeeReceiver.sol
├── IFractionalReserve.sol
├── ILender.sol
├── IMiddleware.sol
├── IMintableERC20.sol
├── IMinter.sol
├── INetwork.sol
├── INetworkMiddleware.sol
├── IOracle.sol
├── IOracleTypes.sol
├── IPriceOracle.sol
├── IRateOracle.sol
├── IRestakerRewardReceiver.sol
├── IScaledToken.sol
├── IStakedCap.sol
├── IStakerRewards.sol
├── IUpgradeableBeacon.sol
├── IVault.sol
├── IVaultAdapter.sol
├── IZapOFTComposer.sol
└── IZapRouter.sol
lendingPool
├── Lender.sol
├── libraries
│   ├── BorrowLogic.sol
│   ├── LiquidationLogic.sol
│   ├── ReserveLogic.sol
│   ├── ValidationLogic.sol
│   ├── ViewLogic.sol
│   ├── configuration
│   │   └── AgentConfiguration.sol
│   └── math
│       ├── MathUtils.sol
│       ├── PercentageMath.sol
│       └── WadRayMath.sol
└── tokens
    ├── DebtToken.sol
    └── base
        ├── MintableERC20.sol
        └── ScaledToken.sol
oracle
├── Oracle.sol
├── PriceOracle.sol
├── RateOracle.sol
└── libraries
    ├── AaveAdapter.sol
    ├── CapTokenAdapter.sol
    ├── ChainlinkAdapter.sol
    ├── StakedCapAdapter.sol
    └── VaultAdapter.sol
storage
├── AccessStorageUtils.sol
├── DebtTokenStorageUtils.sol
├── DelegationStorageUtils.sol
├── FeeAuctionStorageUtils.sol
├── FeeReceiverStorageUtils.sol
├── FractionalReserveStorageUtils.sol
├── LenderStorageUtils.sol
├── MintableERC20StorageUtils.sol
├── MinterStorageUtils.sol
├── NetworkMiddlewareStorageUtils.sol
├── NetworkStorageUtils.sol
├── PriceOracleStorageUtils.sol
├── RateOracleStorageUtils.sol
├── ScaledTokenStorageUtils.sol
├── StakedCapStorageUtils.sol
├── VaultAdapterStorageUtils.sol
└── VaultStorageUtils.sol
token
├── CapToken.sol
├── L2Token.sol
├── OFTLockbox.sol
├── OFTPermit.sol
└── StakedCap.sol
vault
├── FractionalReserve.sol
├── Minter.sol
├── Vault.sol
└── libraries
    ├── FractionalReserveLogic.sol
    ├── MinterLogic.sol
    └── VaultLogic.sol
zap
├── SafeOFTLzComposer.sol
└── ZapOFTComposer.sol
```
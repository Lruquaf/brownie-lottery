from brownie import (
    network,
    accounts,
    config,
    Contract,
    MockV3Aggregator,
    LinkToken,
    VRFCoordinatorMock,
)

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "link_token": LinkToken,
    "vrf_coordinator": VRFCoordinatorMock,
}
DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        return contract
    else:
        if len(contract_type) <= 0:
            deploy_mocks()
        return contract_type[-1]


def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=200000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funded contract with LINK!")
    return tx

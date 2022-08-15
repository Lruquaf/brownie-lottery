import time
from brownie import Lottery, config, network
from scripts.helpful_scripts import fund_with_link, get_account, get_contract


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("link_token").address,
        get_contract("vrf_coordinator").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"The contract deployed at {lottery}")
    return lottery


def start_lottery():
    lottery = Lottery[-1]
    account = get_account()
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    print("The lottery is started!")


def enter_lottery(index):
    account = get_account(id=index)
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print(f"You are {lottery.number_of_players()}. player of the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_tx = lottery.endLottery(2, {"from": account})
    ending_tx.wait(1)
    time.sleep(180)
    for i in range(0, lottery.number_of_winners()):
        print("The " + str(i + 1) + ". winner is " + str(lottery.getWinnerPlayers(i)))


def main():
    deploy_lottery()
    start_lottery()
    for i in ["test1", "test2", "test3", "test4", "test5"]:
        enter_lottery(i)
    end_lottery()

import json
import forta_agent
from forta_agent import Finding, FindingType, FindingSeverity, get_json_rpc_url
from web3 import Web3
import requests

LOW_BALANCE_LOW_PRIORITY = 100000
LOW_BALANCE_MEDIUM_PRIORITY = 10000
LOW_BALANCE_HIGH_PRIORITY = 1000
LOW_BALANCE_CRITICAL_PRIORITY = 100

GRAVITY_CONTRACT_ADDRESS = "0xa4108aA1Ec4967F8b52220a4f7e94A8201F2D906"

with open("./src/ABI/Gravity.json", 'r') as abi_file:  # get abi from the file
    gravity_abi = json.load(abi_file)

with open("./src/ABI/erc20.json", 'r') as abi_file:  # get abi from the file
    erc20_abi = json.load(abi_file)

tbe = next((x for x in gravity_abi if x.get('name', "") == "TransactionBatchExecutedEvent"), None)
web3 = Web3(Web3.HTTPProvider(get_json_rpc_url()))
headers = {
    'accept': 'application/json',
}


def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent):
    findings = []

    for event in transaction_event.filter_log(json.dumps(tbe), GRAVITY_CONTRACT_ADDRESS):
        token_address = event.get('args', {}).get('_token', '')

        if not token_address:
            continue
        token_contract = web3.eth.contract(address=Web3.toChecksumAddress(token_address), abi=erc20_abi)
        balance = token_contract.functions.balanceOf(Web3.toChecksumAddress(GRAVITY_CONTRACT_ADDRESS)).call()
        symbol = token_contract.functions.symbol().call()
        decimals = token_contract.functions.decimals().call()

        balance = balance // 10 ** decimals
        response = requests.get(
            f'https://api.coingecko.com/api/v3/coins/ethereum/contract/{token_address}',
            headers=headers)
        token_price = response.json().get('market_data', {}).get('current_price', {}).get('usd', {})

        if token_price:
            balance_in_usd = balance * token_price
        else:
            balance_in_usd = balance

        if balance_in_usd < LOW_BALANCE_LOW_PRIORITY:
            findings.append(Finding({
                'name': f'Low {symbol} Balance',
                'description': f'There are only {balance} {symbol} tokens left on the balance '
                               f'of the GravityBridge contract',
                'alert_id': 'Gravity-Low-Balance',
                'type': FindingType.Info,
                'severity': get_severity(balance_in_usd),
                'metadata': {
                    'balance': balance,
                    'token_address': token_address
                }
            }))

    return findings


def get_severity(balance):
    if balance < LOW_BALANCE_CRITICAL_PRIORITY:
        return FindingSeverity.Critical
    elif balance < LOW_BALANCE_HIGH_PRIORITY:
        return FindingSeverity.High
    elif balance < LOW_BALANCE_MEDIUM_PRIORITY:
        return FindingSeverity.Medium
    else:
        return FindingSeverity.Low

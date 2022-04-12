# Gravity Bridge Low Balance

## Description

This agent detects when, after using the Cosmos -> Ethereum bridge, the balance of the specified token in USD equivalent 
on the GravityBridge contract falls below a certain value.

## Supported Chains

- Ethereum

## Alerts

Describe each of the type of alerts fired by this agent

- `Gravity-Low-Balance`
  - Fired when the balance of the specified token on 
the GravityBridge contract falls below 100k USD
  - Severity depends on the value:
    - `Low` when the balance is greater than 10k but smaller than 100k
    - `Medium` when the balance is greater than 1k but smaller than 10k
    - `High` when the balance is greater than 100 but smaller than 1k
    - `Critical` when the balance is smaller than 100
  - Metadata contains:
    - `balance`
    - `token_address`

## Test Data

The agent behaviour can be verified changing the balance threshold with the following transactions:

```python
LOW_BALANCE_LOW_PRIORITY = 1000000
```

```python
❯ npx forta-agent@latest run --tx 0x8960b45f313b9218e1346be5c15e1581cdeef305cf3ae1bce879513ac1eb606f
1 findings for transaction 0x8960b45f313b9218e1346be5c15e1581cdeef305cf3ae1bce879513ac1eb606f {
  "name": "Low USDC Balance",
  "description": "There are only 237587 USDC tokens left on the balance of the GravityBridge contract",
  "alertId": "Gravity-Low-Balance",
  "protocol": "ethereum",
  "severity": "Low",
  "type": "Info",
  "metadata": {
    "balance": 237587,
    "token_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
  }
}
```
```python
❯ npx forta-agent@latest run --tx 0xa6eea484015c71f522065291601a0e8724c815d63b3870e00bad7103b5c66651
1 findings for transaction 0xa6eea484015c71f522065291601a0e8724c815d63b3870e00bad7103b5c66651 {
  "name": "Low WETH Balance",
  "description": "There are only 57 WETH tokens left on the balance of the GravityBridge contract",
  "alertId": "Gravity-Low-Balance",
  "protocol": "ethereum",
  "severity": "Low",
  "type": "Info",
  "metadata": {
    "balance": 57,
    "token_address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
  }
}
```
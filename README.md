 This repo has a simple interface to the GDAX trading
 platform for trading cryptocurrencies.

 It has tools for monitoring balances and accounts, for submitting orders, and for running a market maker.

 A `config.py` file with an API key is required to run it:

```
  key = your_key 
  passphrase = your_passphrase 
  secret = your_secret 
  ETH_ACCT = your_ETH_account 
  USD_ACCT = your_USD_account 
  base_url = "https://api.gdax.com"
  risk_limits = {
  'ETH' : 1.0,
  'USD' : 100,
  'BTC' : 0.2,
  'LTC' : 2.0
  }
```

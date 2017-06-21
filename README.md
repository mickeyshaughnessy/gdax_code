# GDAX trading interface

## Usage

```
# Run all unit tests
trader test

# Run the arbitrage strat
trader simulate
```

### Configuration

To enable trading, configure a `config.py` file in the root directory with:

```
key = "your key" 
passphrase = "your passphrase"
secret = "your secret"
ETH_ACCT = "your ETH account"
USD_ACCT = "your USD account"
base_url = "https://api.gdax.com"
```

### GDAX

[Documentation](https://docs.gdax.com/?python#introduction)
* [API](https://docs.gdax.com/?python#requests)
* [Fees](https://docs.gdax.com/?python#fees)
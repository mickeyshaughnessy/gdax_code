import requests
from config import *
from gdax_auth import GdaxAuth
import pprint
from market_maker import get_position, get_bid_ask

def get_accounts(auth=None):
    r = requests.get(base_url + '/accounts', auth=auth)
    return r.json()

def get_usd_ex(currency):
    bid, ask = get_bid_ask(product='%s-USD' % currency) 
    return 0.5 * (bid + ask)

def get_total_balance(auth=None):
    resp = get_accounts(auth=auth)
    balance = 0
    for acct in resp:
        if acct.get('currency') == 'USD':
            usd_ex = 1.0
        else:
            usd_ex = get_usd_ex(acct.get('currency'))
        balance += usd_ex * float(acct.get('balance'))
    return balance

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    resp = get_accounts(auth=auth)
    for acct in resp:
        print 'type: %s, balance: %s, hold: %s, available: %s' % (acct.get('currency'), acct.get('balance'), acct.get('hold'), acct.get('available'))
    print 'Total value is: %s' % get_total_balance(auth=auth)

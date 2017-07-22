import requests
from config import *
from gdax_auth import GdaxAuth
import pprint
from market_maker import get_position, get_bid_ask, get_accounts, get_usd_ex, get_total_balance

#def get_accounts(auth=None):
#    r = requests.get(base_url + '/accounts', auth=auth)
#    return r.json()
#
#def get_usd_ex(currency):
#    bid, ask = get_bid_ask(product='%s-USD' % currency) 
#    return 0.5 * (bid + ask)
#
#def get_total_balance(auth=None):
#    resp = get_accounts(auth=auth)
#    balance, balances = 0, {} 
#    for acct in resp:
#        _balance = float(acct.get('balance'))
#        _currency = acct.get('currency') 
#        if _currency == 'USD':
#            usd_ex = 1.0
#        else:
#            usd_ex = get_usd_ex(_currency)
#        balance += usd_ex * _balance
#        balances[_currency] = _balance
#    return balance, balances

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    resp = get_accounts(auth=auth)
    for acct in resp:
        print 'type: %s, balance: %s, hold: %s, available: %s' % (acct.get('currency'), acct.get('balance'), acct.get('hold'), acct.get('available'))
    total_value, balances = get_total_balance(auth=auth)
    print 'Total value is: %s' % total_value
    print 'Balances: %s' % balances

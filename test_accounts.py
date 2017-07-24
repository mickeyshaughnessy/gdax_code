import requests
from config import *
from gdax_auth import GdaxAuth
import pprint
from market_maker import get_position, get_bid_ask, get_usd_ex, get_total_balance

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    resp = requests.get(base_url + '/accounts', auth=auth)
    for acct in resp.json():
        print 'type: %s, balance: %s, hold: %s, available: %s' % (acct.get('currency'), acct.get('balance'), acct.get('hold'), acct.get('available'))
    total_value, balances = get_total_balance(auth=auth)
    print 'Total value is: %s' % total_value
    print 'Balances: %s' % balances

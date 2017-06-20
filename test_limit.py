import requests
from config import *
from gdax_auth import GdaxAuth
import json
import pprint
import sys
from market_maker import make_limit, cancel_all
import time

def get_safe_sell(auth=None):
    r = requests.get(base_url + '/products/ETH-USD/book', auth=auth)
    return 2 * float(r.json().get('asks')[0][0])

def get_safe_buy(auth=None):
    r = requests.get(base_url + '/products/ETH-USD/book', auth=auth)
    return 0.5 * float(r.json().get('bids')[0][0])

if __name__ == "__main__":
    print 'This may spend real money -- proceed? (y/n)'
    choice = raw_input()
    if choice == 'y':
        auth = GdaxAuth(key, secret, passphrase)
        r = requests.get(base_url + '/orders', auth=auth)
        print 'Orders:'
        pprint.pprint(r.json())
        safe_sell = get_safe_sell(auth=auth)
        safe_buy = get_safe_buy(auth=auth)
        buy_resp = make_limit(side='buy', size=0.1, price=safe_buy, auth=auth)
        sell_resp = make_limit(side='sell', size=0.1, price=safe_sell, auth=auth)
        time.sleep(5)
        r = requests.get(base_url + '/orders', auth=auth)
        print 'Orders:'
        pprint.pprint(r.json())
        cancel_all(auth=auth)
        time.sleep(5)
        r = requests.get(base_url + '/orders', auth=auth)
        print 'Orders:'
        pprint.pprint(r.json())
    else:
        sys.exit()

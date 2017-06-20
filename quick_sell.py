# This script submits a one-time sell limit order at near market price

import requests
from config import *
from gdax_auth import GdaxAuth
import pprint
import sys
from market_maker import make_limit

def get_good_sell(auth=None):
    r = requests.get(base_url + '/products/ETH-USD/book', auth=auth)
    return 1.005 * float(r.json().get('asks')[0][0])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'input the order size as `python quick_sell.py <size>`'
        sys.exit()
    print 'This may spend real money -- proceed? (y/n)'
    choice = raw_input()
    if choice == 'y':
        auth = GdaxAuth(key, secret, passphrase)
        good_sell = get_good_sell(auth=auth)
        sell_resp = make_limit(side='sell', size=float(sys.argv[1]), price=good_sell, auth=auth)
        pprint.pprint(sell_resp)
    else:
        sys.exit()

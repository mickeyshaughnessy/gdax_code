import requests
from config import *
from gdax_auth import GdaxAuth
import pprint
from market_maker import get_position

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    r = requests.get(base_url + '/accounts', auth=auth)
    resp = r.json()
    for acct in resp:
        print 'type: %s, balance: %s, hold: %s, available: %s' % (acct.get('currency'), acct.get('balance'), acct.get('hold'), acct.get('available'))

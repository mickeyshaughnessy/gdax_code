import requests
from config import *
from gdax_auth import GdaxAuth
import json
from market_maker import cancel_all, make_limit
from test_limit import get_safe
import pprint
import json

if __name__ == "__main__":
    print 'This may spend real money -- proceed? (y/n)'
    choice = raw_input()
    if choice == 'y':
        auth = GdaxAuth(key, secret, passphrase)
        # make a sell order at 2x the bid
        safe = get_safe()
        resp = make_limit(side='sell', size=0.1, price=safe, auth=auth)
        print resp
        raw_input()
        r = requests.get(base_url + '/orders/', auth=auth)
        print pprint.pprint(r.json())
        resp = cancel_all(auth=auth)
        print resp
        raw_input()
        r = requests.get(base_url + '/orders/', auth=auth)
        print pprint.pprint(r.json())
    else:
        sys.exit()

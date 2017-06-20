import requests
from config import *
from gdax_auth import GdaxAuth
import json
import pprint
import sys

def get_safe(auth=None):
    r = requests.get(base_url + '/products/ETH-USD/book', auth=auth)
    return 2 * float(r.json().get('bids')[0][0])

if __name__ == "__main__":
    print 'This may spend real money -- proceed? (y/n)'
    choice = raw_input()
    if choice == 'y':
        auth = GdaxAuth(key, secret, passphrase)
        safe = get_safe()
        order = json.dumps({
                'side' : 'sell',
                'product_id' : 'ETH-USD',
                'size' : 0.1234,
                'price' : safe 
                })
        r = requests.post(base_url + '/orders', data=order, auth=auth)
        print pprint.pprint(r.json())
    
    else:
        sys.exit()

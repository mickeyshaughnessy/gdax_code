import requests
from config import *
from gdax_auth import GdaxAuth
import json

if __name__ == "__main__":
    print 'This may spend real money -- proceed? (y/n)'
    choice = raw_input()
    if choice == 'y':
        auth = GdaxAuth(key, secret, passphrase)
        order = json.dumps({
                'side' : 'sell',
                'product_id' : 'ETH-USD',
                'size' : 0.1234,
                'price' : 380
                })
        r = requests.post(base_url + '/orders', data=order, auth=auth)
        print r.json()
    
    else:
        sys.exit()

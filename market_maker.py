# This script buys low and sells high
import requests
from config import *
import json

def get_position(product='ETH', auth=None):
    r = requests.get(base_url + '/position/', auth=auth) 
    resp = r.json()
    return float(resp['accounts'][product].get(hold))

def cancel_all(auth=None):
    r = requests.delete(base_url + '/orders', auth=auth)

def make_limit(side='buy', size=0.0, price=0.0, product='ETH-USD', auth=None):
    order = json.dumps({
            'side' : side,
            'product_id' : product,
            'size' : size,
            'price' : price 
            })
    r = requests.post(base_url + '/orders', data=order, auth=auth)
    return r.json()

def get_bid_ask(product='ETH-USD'):
    r = requests.get(base_url + '/products/%s/book' % product)
    resp = r.json()
    bid = float(resp['bids'][0][0])
    ask = float(resp['asks'][0][0])
    return bid, ask
    

def make_market():
    auth = GdaxAuth(key, secret, passphrase)
    while True:
        sleep(1)
        eth_pos = get_position(product='ETH', auth=auth)
        usd_pos = get_position(product='USD', auth=auth)
        bid, ask = get_bid_ask()
        print 'ETH_pos = %s, USD_pos = %s, bid/ask = %s - %s' % (eth_pos, usd_pos, bid, ask)
        if eth_pos < 0.1 and usd_pos < 50: # ETH / USD
            make_limit(side='buy', size = 0.01, price=0.99*bid) 
            make_limit(side='sell', size = 0.01, price=1.01*bid) 
        elif eth_pos < 0.1:
            make_limit(side='buy', size = 0.01, price=0.99*bid)
        elif usd_pos < 50:
            make_limit(side='sell', size = 0.01, price=1.01*bid)
        else:
            cancel_all()

if __name__ == "__main__":
    make_market() 

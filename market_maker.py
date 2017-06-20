# This script buys low and sells high
import requests
from config import *
import json
import sys

def get_position(product='ETH', auth=None):
    r = requests.get(base_url + '/position/', auth=auth) 
    resp = r.json()
    return float(resp['accounts'][product].get('hold'))

def cancel_all(auth=None):
    r = requests.delete(base_url + '/orders', auth=auth)

def make_limit(side='buy', size=0.0, price=0.0, product='ETH-USD', auth=None):
    price = (int(price * 100))/100.0 # GDAX API only takes two decimal places on prices, apparently.
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
    

def make_market(product='ETH-USD'):
    A = product.split('-')[0]
    B = product.split('-')[1]
    auth = GdaxAuth(key, secret, passphrase)
    while True:
        sleep(1)
        A_pos = get_position(product=A, auth=auth)
        B_pos = get_position(product=B, auth=auth)
        bid, ask = get_bid_ask(product)
        print '%s_pos = %s, %s_pos = %s, bid/ask = %s - %s' % (A, A_pos, B, B_pos, bid, ask)
        if A_pos < risk_limits[A] and B_pos < risk_limits[B]: 
            make_limit(side='buy', size = 0.01, price=0.99*bid, product=product) 
            make_limit(side='sell', size = 0.01, price=1.01*bid, product=product) 
        elif A_pos < risk_limits[A]:
            make_limit(side='buy', size = 0.01, price=0.99*bid, product=product)
        elif B_pos < risk_limits[B]:
            make_limit(side='sell', size = 0.01, price=1.01*bid, product=product)
        else:
            cancel_all()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        product = sys.argv[1]
    else:
        product = 'ETH-USD'
    make_market(product=product) 

# This script buys low and sells high
import requests
from config import *
import json
import sys
from gdax_auth import GdaxAuth
from time import sleep
from pprint import pprint
import random

def get_position(product='ETH', auth=None):
    r = requests.get(base_url + '/position/', auth=auth) 
    resp = r.json()
    return float(resp['accounts'][product].get('hold'))

def cancel_all(auth=None):
    r = requests.delete(base_url + '/orders', auth=auth)
    return r.json()

def make_limit(side='buy', size=0.0, price=0.0, product='ETH-USD', auth=None):
    price = (int(price * 100))/100.0 # GDAX API only takes two decimal places on prices, apparently.
    order = json.dumps({
            'side' : side,
            'product_id' : product,
            'size' : size,
            'price' : price 
            })
    r = requests.post(base_url + '/orders', data=order, auth=auth)
    print 'submitted order to %s %s %s at %s' % (side, size, product, price)
    return r.json()

def get_bid_ask(product='ETH-USD'):
    r = requests.get(base_url + '/products/%s/book' % product)
    resp = r.json()
    bid = float(resp['bids'][0][0])
    ask = float(resp['asks'][0][0])
    return bid, ask

 
def make_market(product='ETH-USD', auth=None):
    A = product.split('-')[0]
    B = product.split('-')[1]
    margin = 0.002
    noise = 0.001
    while True:
        sleep(5)
        A_pos = get_position(product=A, auth=auth)
        B_pos = get_position(product=B, auth=auth)
        bid, ask = get_bid_ask(product)
        buy_price = (1 - margin + random.random()*noise) * bid
        sell_price = (1 + margin + random.random()*noise) * ask 
        print '%s_pos = %s, %s_pos = %s, bid/ask = %s - %s, spread = %s, mySpread = %s' % (
            A, A_pos, B, B_pos, bid, ask, ask-bid, sell_price - buy_price
        )
        if A_pos < risk_limits[A] and B_pos < risk_limits[B]: 
            make_limit(side='buy', size = 0.01, price=buy_price, product=product, auth=auth) 
            make_limit(side='sell', size = 0.01, price=sell_price, product=product, auth=auth) 
        elif B_pos < risk_limits[B]:
            make_limit(side='buy', size = 0.01, price=buy_price, product=product, auth=auth)
        elif A_pos < risk_limits[A]:
            make_limit(side='sell', size = 0.01, price=sell_price, product=product, auth=auth)
        else:
            cancel_all()

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    if len(sys.argv) > 1:
        product = sys.argv[1]
    else:
        product = 'ETH-USD'
    make_market(product=product,auth=auth) 

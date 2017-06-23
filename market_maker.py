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

def cancel_product(product='ETH-USD', auth=None):
    o = requests.get(base_url + '/orders?product_id=%s' % product, auth=auth)
    for order in o.json():
        r = requests.delete(base_url + '/orders/%s' % order['id'], auth=auth)

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
    print 'submitted order to %s %s %s at %s %s' % (side, size, product.split('-')[0], price, product.split('-')[1])
    return r.json()

def get_bid_ask(product='ETH-USD'):
    r = requests.get(base_url + '/products/%s/book' % product)
    resp = r.json()
    bid = float(resp['bids'][0][0])
    ask = float(resp['asks'][0][0])
    return bid, ask

def get_buy_sell(product='ETH-USD'):
    spread_factor = 1.8 # How big to make mySpread relative to the market
    noise = 0.1 # noisy additional spread
    gdax_bid, gdax_ask = get_bid_ask(product=product)
    gdax_spread = gdax_ask - gdax_bid
    buy_price = gdax_bid - 0.5 * gdax_spread * (spread_factor + noise * random.random())
    sell_price = gdax_ask + 0.5 * gdax_spread * (spread_factor + noise * random.random())
    return (buy_price, sell_price)

def make_market(product='ETH-USD', auth=None):
    A = product.split('-')[0]
    B = product.split('-')[1]
    _size = 0.25 # how big to make the orders 
    while True:
        sleep(3)
        cancel_product(live_buys, live_sells, product=product, auth=auth)
        sleep(2)
        A_pos = get_position(product=A, auth=auth)
        B_pos = get_position(product=B, auth=auth)
        buy_price, sell_price = get_buy_sell(product=product)
        print '%s_at_risk = %s, %s_at_risk = %s, mySpread = %s' % (
            A, A_pos, B, B_pos, sell_price - buy_price
        )
        if A_pos < risk_limits[A] and B_pos < risk_limits[B]: 
            buy = make_limit(side='buy', size=_size, price=buy_price, product=product, auth=auth) 
            sell = make_limit(side='sell', size=_size, price=sell_price, product=product, auth=auth) 
        elif B_pos < risk_limits[B]:
            buy = make_limit(side='buy', size=_size, price=buy_price, product=product, auth=auth)
            sell = None
        elif A_pos < risk_limits[A]:
            sell = make_limit(side='sell', size=_size, price=sell_price, product=product, auth=auth)
            buy = None
        else:
            cancel_all(auth=auth)
        if buy:
            if buy.get('message'):
                print buy.get('message')
            else:
                live_buys.append(buy.get('id'))
        if sell:
            if sell.get('message'):
                print sell.get('message')
            else:
                live_sells.append(sell.get('id'))

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    product = sys.argv[1]
    make_market(product=product,auth=auth) 

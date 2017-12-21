# This script buys low and sells high
import requests
from config import *
import json
import sys
from gdax_auth import GdaxAuth
from time import sleep
from pprint import pprint
import random
import argparse

def get_position(product='ETH', auth=None):
    r = requests.get(base_url + '/position/', auth=auth) 
    resp = r.json()
    return float(resp['accounts'][product].get('hold'))

def cancel_product(product='ETH-USD', auth=None):
    o = requests.get(base_url + '/orders?product_id=%s' % product, auth=auth)
    for order in o.json():
        r = requests.delete(base_url + '/orders/%s' % order.get('id'), auth=auth)

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

def get_buy_sell(product='ETH-USD', spread_factor=2.8, noise=0.1):
    # spread_factor: How big to make mySpread relative to the market
    # noise: noisy additional spread
    gdax_bid, gdax_ask = get_bid_ask(product=product)
    gdax_spread = gdax_ask - gdax_bid
    # here, get other exchange bid/ask prices to determine "fair" value
    buy_price = gdax_bid - 0.5 * gdax_spread * (spread_factor + noise * random.random())
    sell_price = gdax_ask + 0.5 * gdax_spread * (spread_factor + noise * random.random())
    return (buy_price, sell_price)

def make_market(product='ETH-USD', auth=None, order_size=0.25):
    cancel_all(auth=auth)
    (A, B) = product.split('-')[-2:]
    live_buys, live_sells = [], []
    while True:
        sleep(4)
        A_pos, B_pos = get_position(product=A, auth=auth), get_position(product=B, auth=auth)
        if random.random() < 0.02: cancel_product(auth=auth)
        buy_price, sell_price = get_buy_sell(product=product)
        print '%s_at_risk = %s, %s_at_risk = %s, mySpread = %s' % (
            A, A_pos, B, B_pos, sell_price - buy_price
        )
        if A_pos < risk_limits[A] and B_pos < risk_limits[B]: 
            buy = make_limit(side='buy', size=order_size, price=buy_price, product=product, auth=auth) 
            sell = make_limit(side='sell', size=order_size, price=sell_price, product=product, auth=auth) 
        elif B_pos < risk_limits[B]:
            buy = make_limit(side='buy', size=order_size, price=buy_price, product=product, auth=auth)
            sell = None
        elif A_pos < risk_limits[A]:
            sell = make_limit(side='sell', size=order_size, price=sell_price, product=product, auth=auth)
            buy = None
        else:
            cancel_product(product=product, auth=auth)
            live_buys, live_sells = [], []
        
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--product', type=str, default='ETH-USD', help='THE CURRENCY PAIR!')
    parser.add_argument('-s', '--size', type=float, default=0.1, help='crypto side order size')
    args = parser.parse_args()
    auth = GdaxAuth(key, secret, passphrase)
    make_market(product=args.product, auth=auth, order_size=args.size) 

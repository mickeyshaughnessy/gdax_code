# This script buys low and sells high
import requests, json, sys, random, argparse
from config import *
from gdax_auth import GdaxAuth
from time import sleep
from pprint import pprint

def get_usd_ex(currency):
    bid, ask = get_bid_ask(product='%s-USD' % currency)
    return 0.5 * (bid + ask)

def get_total_balance(auth=None):
    resp = requests.get(base_url + '/accounts', auth=auth) 
    balance, balances = 0, {}
    for acct in resp.json():
        _balance = float(acct.get('balance'))
        _currency = acct.get('currency')
        if _currency == 'USD':
            usd_ex = 1.0
        else:
            usd_ex = get_usd_ex(_currency)
        balance += usd_ex * _balance
        balances[_currency] = _balance
    return balance, balances

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
    resp = requests.get(base_url + '/products/%s/book' % product)
    bid = float(resp.json()['bids'][0][0])
    ask = float(resp.json()['asks'][0][0])
    return bid, ask

def get_buy_sell(product='ETH-USD', spread_factor=5.8, noise=0.1):
    # spread_factor: How big to make mySpread relative to the market
    # noise: noisy additional spread
    gdax_bid, gdax_ask = get_bid_ask(product=product)
    gdax_spread = gdax_ask - gdax_bid
    # here, get other exchange bid/ask prices to determine "fair" value
    buy_price = gdax_bid - 0.5 * gdax_spread * (spread_factor + noise * random.random())
    sell_price = gdax_ask + 0.5 * gdax_spread * (spread_factor + noise * random.random())
    return (buy_price, sell_price)

def is_unbalanced(auth=None, product='LTC-USD'):
    currency = product.split('-')[0]
    ex = get_usd_ex(currency)
    _, balances = get_total_balance(auth=auth)
    A_bal, B_bal = balances.get(currency, 0.0), balances.get('USD', 0.0)
    A_val = A_bal * ex
    if A_val < 0.2 * B_bal:
        return True, {'USD':B_bal}, {currency:A_bal}, ex
    elif A_val > 5 * B_bal:
        return True, {currency:A_bal}, {'USD':B_bal}, ex
    else:
        return False, {}, {}, ex

def rebalance(auth=None, product='LTC-USD'):
    condition, strong, weak, ex = is_unbalanced(auth=auth, product=product) 
    while condition:
        cancel_all(auth=auth)
        bid, ask = get_bid_ask(product)
        if 'USD' in strong.keys():
            make_limit(
                side='buy',
                price=0.98*bid, 
                size=0.5*strong.get('USD')/ex, 
                product=product, 
                auth=auth
            ) 
        else:
            make_limit(
                side='sell',
                price=1.02*ask, 
                size=0.5*strong.values()[0], 
                product=product, 
                auth=auth
            )
        print 'submitted rebalancing order' 
        sleep(20)
        condition, strong, weak, ex = is_unbalanced(auth=auth, product=product)
        
def make_market(product='ETH-USD', auth=None, order_size=0.25, start_A=0, start_B=0, start_ex=0):
    cancel_all(auth=auth)
    (A, B) = product.split('-')[-2:]
    live_buys, live_sells = [], []
    while True:
        _, balances = get_total_balance(auth=auth)
        print 'change in %s: %s, change in %s: %s, total_earnings: %s' % (A, balances[A] * start_ex - start_A, B, balances[B] - start_B, balances[A] * start_ex  - start_A + balances[B] - start_B)
        sleep(4)
        A_pos, B_pos = get_position(product=A, auth=auth), get_position(product=B, auth=auth)
        if random.random() < 0.08: cancel_product(auth=auth)
        if random.random() < 0.2: rebalance(auth=auth, product=product)
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
    (A, B) = args.product.split('-')[-2:]
    _, balances = get_total_balance(auth=auth)
    start_ex = get_usd_ex(A)
    start_value_A, start_value_B = balances[A] * start_ex, balances[B] 
    make_market(product=args.product, auth=auth, order_size=args.size, start_A=start_value_A, start_B=start_value_B, start_ex=start_ex) 

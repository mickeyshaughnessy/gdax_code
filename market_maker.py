# This script buys low and sells high
import requests
from config import *
import json

def get_position():
    # return the total outstanding risk
    return 0.0

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

def make_market():
    while True:
        sleep(1)
        pos = get_position()
        bid_ask = get_bid_ask()
        if abs(pos) < 500: #USD
            # put in two sided limit order
			pass
        else:
            cancel_all()


if __name__ == "__main__":
    make_market() 

import requests
from config import *
from gdax_auth import GdaxAuth

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    r = requests.get(base_url + '/products/ETH-USD/book?level=2', auth=auth)
    print 'ETH book is: %s' % r.json()
    r = requests.get(base_url + '/products/ETH-USD/book', auth=auth)
    bid = r.json().get('bids')[0][0]
    ask = r.json().get('asks')[0][0]
    print 'ETH bid - ask is: %s/%s --> %s' % (bid, ask, float(ask) - float(bid))

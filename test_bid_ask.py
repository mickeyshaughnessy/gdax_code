import requests
from config import *
from gdax_auth import GdaxAuth
import pprint
from market_maker import get_bid_ask

if __name__ == "__main__":
    resp = get_bid_ask()
    print resp
    print 'bid: %s, ask: %s' % (resp[0], resp[1])

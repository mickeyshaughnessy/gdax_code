import requests
from config import *
from gdax_auth import GdaxAuth
import pprint
from market_maker import get_position

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    resp = get_position(auth)
    print '---- Position ----'
    pprint.pprint(resp)

import requests
from config import *
from gdax_auth import GdaxAuth
import pprint

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    r = requests.get(base_url + '/position/', auth=auth)
    print '---- Position ----'
    pprint.pprint(r.json())
    r = requests.get(base_url + '/orders/', auth=auth)
    print '---- Orders ----'
    print pprint.pprint(r.json())

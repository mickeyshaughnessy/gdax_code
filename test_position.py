import requests
from config import *
from gdax_auth import GdaxAuth
import pprint

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    r = requests.get(base_url + '/position/', auth=auth)
    resp = r.json()
    print '---- Position ----'
    pprint.pprint(resp)

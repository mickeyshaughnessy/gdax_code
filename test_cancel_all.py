import requests
from config import *
from gdax_auth import GdaxAuth
import json
from market_maker import cancel_all
import pprint
import json
import time

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    resp = cancel_all(auth=auth)
    print pprint.pprint(resp)

import requests
from config import *
from gdax_auth import GdaxAuth

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    r = requests.get(base_url + '/accounts/', auth=auth)
    r = requests.get(base_url + '/accounts/' + ETH_ACCT, auth=auth)
    print 'ETH balance is: %s' % r.json().get('balance')
    r = requests.get(base_url + '/accounts/' + USD_ACCT, auth=auth)
    print 'USD balance is: %s' % r.json().get('balance')

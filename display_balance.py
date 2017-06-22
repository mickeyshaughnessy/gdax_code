from test_accounts import get_total_balance
from time import sleep
from gdax_auth import GdaxAuth
from config import *

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    while True:
        print 'Total balance ($): %s' % get_total_balance(auth=auth)
        sleep(5)

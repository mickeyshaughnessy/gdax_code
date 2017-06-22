from test_accounts import get_total_balance
from time import sleep
from gdax_auth import GdaxAuth
from config import *
from datetime import datetime as dt

epoch = dt.utcfromtimestamp(0)

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    while True:
        with open('balances.dat', 'a') as f:
            balance = get_total_balance(auth=auth)
            ts = (dt.now() - epoch).total_seconds() 
            print 'Total balance ($): %s' % get_total_balance(auth=auth)
            f.write('%s %s\n' % (balance, ts))
            sleep(5)

from test_accounts import get_total_balance
from time import sleep
from gdax_auth import GdaxAuth
from config import *
from datetime import datetime as dt

epoch = dt.utcfromtimestamp(0)

if __name__ == "__main__":
    auth = GdaxAuth(key, secret, passphrase)
    start_balance, _ = get_total_balance(auth=auth)
    while True:
        with open('balances.dat', 'a') as f:
            balance, balances = get_total_balance(auth=auth)
            ts = (dt.now() - epoch).total_seconds() 
            print 'Total balance ($): %s      change ($): %s' % (balance, start_balance - balance) 
            print 'Balances : %s' % balances 
            f.write('%s %s\n' % (balance, ts))
            sleep(5)

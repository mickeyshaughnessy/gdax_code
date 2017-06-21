import requests
from config import GDAX_BASE_URL
from models.constants import PRODUCT_ETH_TO_USD
from models.admin import Order, OrderBook
from bootstrap import logger

SEQUENCE_NUMBER = None

def track_sequence_number(latest_sequence_number):
    global SEQUENCE_NUMBER
    if SEQUENCE_NUMBER is None:
        SEQUENCE_NUMBER = latest_sequence_number
    elif SEQUENCE_NUMBER > latest_sequence_number:
        #raise Exception("Latest message from GDAX is out of order (expected > %s, but was %s)" % (SEQUENCE_NUMBER, latest_sequence_number))
        logger.debug("Latest message from GDAX is out of order (expected > %s, but was %s)" % (
                SEQUENCE_NUMBER, latest_sequence_number)) #maybe only applies to the web socket feed. what implications does it have here, though?
    else:
        SEQUENCE_NUMBER = latest_sequence_number

class GDAX(object):

    @staticmethod
    def get_order_book(product_id):
        resp = requests.get(GDAX_BASE_URL + '/products/%s/book' % product_id).json()
        track_sequence_number(resp['sequence'])

        bids = map(lambda b: Order(
            price=float(b[0]),
            size=float(b[1]),
            number=int(b[2])
        ), resp['bids'])

        asks = map(lambda b: Order(
             price=float(b[0]),
             size=float(b[1]),
             number=int(b[2])
         ), resp['asks'])

        return OrderBook(bids=list(bids), asks=list(asks))

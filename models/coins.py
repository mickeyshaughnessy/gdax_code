from services.http import GDAX
from models.constants import *
from bootstrap import logger

class Coin(object):
    def __init__(self, quantity):
        self.quantity = float(quantity)

    def to(self, other_coin):
        """
        Need to account for SIZE/NUMBER
        
        We would waterfall starting at the best ask
        :param other_coin: 
        :return:
        """
        if type(self) == LTC and other_coin == BTC:
            best_ask = GDAX.get_order_book(PRODUCT_LTC_TO_BTC).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, "BTC", "LTC"))
            return BTC(quantity= self.quantity*best_ask.price)
        elif type(self) == BTC and other_coin == LTC:
            best_ask = GDAX.get_order_book(PRODUCT_LTC_TO_BTC).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, other_coin, self))
            return LTC(quantity=self.quantity/best_ask.price)

        elif type(self) == USD and other_coin == BTC:
            best_ask = GDAX.get_order_book(PRODUCT_BTC_TO_USD).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, other_coin, self))
            return BTC(quantity=self.quantity / best_ask.price)
        elif type(self) == BTC and other_coin == USD:
            best_ask = GDAX.get_order_book(PRODUCT_BTC_TO_USD).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, other_coin, self))
            return USD(quantity=best_ask.price*self.quantity)

        elif type(self) == USD and other_coin == LTC:
            best_ask = GDAX.get_order_book(PRODUCT_LTC_TO_USD).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, other_coin, self))
            return LTC(quantity=self.quantity / best_ask.price)
        elif type(self) == LTC and other_coin == USD:
            best_ask = GDAX.get_order_book(PRODUCT_LTC_TO_USD).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, other_coin, self))
            return USD(quantity=best_ask.price*self.quantity)

        elif type(self) == USD and other_coin == ETH:
            best_ask = GDAX.get_order_book(PRODUCT_ETH_TO_USD).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, other_coin, self))
            return ETH(quantity=self.quantity / best_ask.price)
        elif type(self) == ETH and other_coin == USD:
            best_ask = GDAX.get_order_book(PRODUCT_ETH_TO_USD).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, other_coin, self))
            return USD(quantity=best_ask.price*self.quantity)

        elif type(self) == ETH and other_coin == BTC:
            best_ask = GDAX.get_order_book(PRODUCT_ETH_TO_BTC).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, other_coin, self))
            return BTC(quantity=best_ask.price*self.quantity)
        elif type(self) == BTC and other_coin == ETH:
            best_ask = GDAX.get_order_book(PRODUCT_ETH_TO_BTC).asks[0]
            logger.debug("Best ask is %s -- %s/%s" % (best_ask.price, other_coin, self))
            return ETH(quantity=self.quantity/best_ask.price)

        else:
            raise Exception("Can't directly convert %s to %s" % (self, other_coin))

class BTC(Coin):
    pass

class LTC(Coin):
    pass

class ETH(Coin):
    pass

class USD(Coin):
    pass
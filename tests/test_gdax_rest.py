import unittest
from services.http import GDAX
from models.constants import PRODUCT_ETH_TO_USD, PRODUCT_BTC_TO_USD, \
    PRODUCT_ETH_TO_BTC, PRODUCT_LTC_TO_USD, PRODUCT_LTC_TO_BTC
from bootstrap import logger

class TestGdaxRest(unittest.TestCase):
    def test_public_endpoints_basic(self):
        for product_id in [
            PRODUCT_ETH_TO_USD,
            PRODUCT_BTC_TO_USD,
            PRODUCT_ETH_TO_BTC,
            PRODUCT_LTC_TO_USD,
            PRODUCT_LTC_TO_BTC
        ]:
            bid, ask = GDAX.get_bid_ask(product_id)
            logger.info("%s price gap is %s" % (product_id, str(bid.price - ask.price)))
            self.assertLess(bid.price, ask.price)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGdaxRest)
    unittest.TextTestRunner(verbosity=1).run(suite)

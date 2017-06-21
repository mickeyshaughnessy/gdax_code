class Order(object):
    def __init__(self, price, size, number):
        self.price, self.size, self.number = price, size, number

    def invert(self):
        """
        O1 -> r1 0.01685, q1 338.823558
        O2 = O1_inv --> r2 q2
        
        r2 = (1/r1)
        q2 = (q1 * r1^2)
        :return: 
        """
        return Order(
            price=1. / self.price,
            size=self.size * self.price ** 2,
            number=self.number
        )

class GDAXConfig(object):
    def __init__(self, key, secret, passphrase):
        self.key, self.secret, self.passphrase = key, secret, passphrase

class OrderBook(object):
    def __init__(self, bids, asks):
        self.bids, self.asks = bids, asks

    def invert(self):
        bids = list(map(lambda order: order.invert(), self.bids))
        asks = list(map(lambda order: order.invert(), self.asks))
        return OrderBook(
            bids=bids,
            asks=asks
        )
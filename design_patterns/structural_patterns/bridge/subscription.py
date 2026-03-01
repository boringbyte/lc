from abc import ABC, abstractmethod

from dateutil.relativedelta import relativedelta


class Subscription(ABC):

    def __init__(self, subscriber, enrolled, discount):
        self._subscriber = subscriber
        self._enrolled = enrolled
        self._discount = discount()

    @property
    def subscriber(self):
        return self._subscriber

    @property
    def enrolled(self):
        return self._enrolled

    @property
    @abstractmethod
    def price_base(self):
        pass

    @property
    def price(self):
        discount = self._discount.discount
        return self.price_base * (1 - discount/100)

    @property
    @abstractmethod
    def expiration(self):
        pass


class Monthly(Subscription):

    @property
    def price_base(self):
        return 50.00

    @property
    def expiration(self):
        return self._enrolled + relativedelta(months=1)


class Annual(Subscription):

    @property
    def price_base(self):
        return 250.00

    @property
    def expiration(self):
        return self._enrolled + relativedelta(years=1)

from design_patterns.structural_patterns.bridge.subscription import Monthly, Annual
from datetime import datetime
from discount import NoDiscount, StudentDiscount, CorporateDiscount


def main():
    # sub1 = Monthly('Bob', datetime.today())
    # sub2 = Annual('Carol', datetime.today())

    sub1 = Monthly('Bob', datetime.today(), StudentDiscount)
    sub2 = Annual('Carol', datetime.today(), CorporateDiscount)
    sub3 = Annual('Ted', datetime.today(), NoDiscount)

    print(f'Subscriber: {sub1.subscriber}, Cost: {sub1.price}, Expiration: {sub1.expiration}')
    print(f'Subscriber: {sub2.subscriber}, Cost: {sub2.price}, Expiration: {sub2.expiration}')
    print(f'Subscriber: {sub3.subscriber}, Cost: {sub3.price}, Expiration: {sub3.expiration}')


if __name__ == '__main__':
    """
    Problem Statement: Lets say, we were asked to create student and corporate discounts of 90% and 80% respectively.
    1. We can solve this problem by creating MonthlyStudent, AnnualStudent, MonthlyCorporate and AnnualCorporate classes
       which subclass from Monthly and Annual subclasses.
    Issues with above statement:
    1. Class Explosion if we need to add more type of discounts or subscriptions.
    2. Duplicate code which breaks DRY principle
    3. Too much code to maintain
    Bridge Pattern:
    Decouple an abstraction from its implementation so that the two can vary independently.
    After adding Discount class, we have another requirement of extended special offers that extend subscription periods
    To solve this problem, we should remove expiration and create Expiration class similar to Discount class
    """
    main()

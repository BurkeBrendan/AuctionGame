import random
import numpy

class Employee:
    strategy = "Random"
    def __init__(self, business, potential_hires):
        self.accept_amount = 5 * random.Random().randrange(1, 20)
        self.hired = False

    def accept_offer(self, amount):
        if amount is self.accept_amount:
            return True
        else:
            return False

class RandomSkewHigh(Employee):
    strategy = "Random Skew High"
    def __init__(self, business, potential_hires):
        Employee.__init__(self, business, potential_hires)
        self.accept_amount = 5 * int(numpy.round(numpy.random.normal(15.0, 2.5)))
        if self.accept_amount < 0:
            self.accept_amount = 0
        elif self.accept_amount > 95:
            self.accept_amount = 95

class RandomSkewLow(Employee):
    strategy = "Random Skew Low"
    def __init__(self, business, potential_hires):
        Employee.__init__(self, business, potential_hires)
        self.accept_amount = 5 * int(numpy.round(numpy.random.normal(5.0, 2.5)))
        if self.accept_amount < 0:
            self.accept_amount = 0
        elif self.accept_amount > 95:
            self.accept_amount = 95

class Eager(Employee):
    strategy = "Eager"
    def __init__(self, business, potential_hires):
        Employee.__init__(self, business, potential_hires)
        self.bus = business
        self.accept_amount = 100

    def accept_offer(self, amount):
        if self.bus.get_num_employees() > 0 and not self.hired:
            self.accept_amount = amount
            return True
        else:
            return False

class Risky(Employee):
    strategy = "Risky"
    def __init__(self, business, potential_hires):
        Employee.__init__(self, business, potential_hires)
        self.bus = business
        self.accept_amount = 100

    def accept_offer(self, amount):
        if self.bus.get_num_employees() > 20 and not self.hired:
            self.accept_amount = amount
            return True
        else:
            return False

class Balanced(Employee):
    strategy = "Balanced"
    def __init__(self, business, potential_hires):
        Employee.__init__(self, business, potential_hires)
        self.bus = business
        self.accept_amount = 100

    def accept_offer(self, amount):
        if self.bus.get_num_employees() > 12 and not self.hired:
            self.accept_amount = amount
            return True
        else:
            return False

class Buddy(Employee):
    strategy = "Buddy"
    def __init__(self, business, hires_list):
        Employee.__init__(self, business, hires_list)
        self.hires_list = hires_list
        self.buddy_index = random.Random().randrange(0, 50)

    def accept_offer(self, amount):
        if self.hires_list[self.buddy_index].hired and not self.hired:
            self.accept_amount = amount
            return True
        else:
            return False

class Asshole(Employee):
    strategy = "Jealous"

    def __init__(self, business, hires_list):
        Employee.__init__(self, business, hires_list)
        self.hires_list = hires_list
        self.buddy_index = random.Random().randrange(0, 50)

    def accept_offer(self, amount):
        if amount >= self.hires_list[self.buddy_index].accept_amount + 20 and not self.hired:
            self.accept_amount = amount
            return True
        else:
            return False

class Greedy(Employee):
    strategy = "Greedy"

    def __init__(self, business, hires_list):
        Employee.__init__(self, business, hires_list)
        self.hires_list = hires_list
        self.accept_amount = 95

    def accept_offer(self, amount):
        if amount >= self.accept_amount:
            return True
        else:
            return False
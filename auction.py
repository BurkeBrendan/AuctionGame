from employee import *
import random
import math
import matplotlib.pyplot as plt

stratClasses = [Employee, RandomSkewLow, RandomSkewHigh, Risky]
MAX_EMPLOYEES = 40
HIRE_POOL = 50
NUM_TRIALS = 1000


class Business:
    def __init__(self):
        self.offer = 5
        self.cutoff = 0
        self.employees = []


    def update_employees(self, employee_list):
        if len(self.employees) >= MAX_EMPLOYEES:
            return
        if len(self.employees) + len(employee_list) > MAX_EMPLOYEES:
            employee_list = employee_list[0: (MAX_EMPLOYEES - len(self.employees))]
        for emp in employee_list:
            emp.hired = True
        self.employees = self.employees + employee_list
        if len(self.employees) >= MAX_EMPLOYEES:
            self.cutoff = self.offer

    def update_offer(self):
        if self.offer < 100:
            self.offer = self.offer + 5
        else:
            self.offer = 100

    def get_num_employees(self):
        return len(self.employees)

def init_trial():
    bus = Business()
    potential_hires = []
    num_strat = [0] * len(stratClasses)
    for i in range(0, HIRE_POOL):
        strat = random.Random().randrange(0,len(stratClasses))
        for j in range(0, len(stratClasses)):
            if strat is j:
                potential_hires.append(stratClasses[j](bus, potential_hires))
                num_strat[j] = num_strat[j] + 1

    return bus, potential_hires, num_strat

def init_trial2(number_optimized):
    bus = Business()
    potential_hires = []
    num_strat = [0] * len(stratClasses)
    for i in range(0, HIRE_POOL - number_optimized):
        strat = random.Random().randrange(0,3)
        for j in range(0, 3):
            if strat is j:
                potential_hires.append(stratClasses[j](bus, potential_hires))
                num_strat[j] = num_strat[j] + 1

    for i in range(0, number_optimized):
        potential_hires.append(Risky(bus, potential_hires))
        num_strat[3] = num_strat[3] + 1

    return bus, potential_hires, num_strat

def run_trial():
    bus, potential_hires, num_strat = init_trial()
    for i in range(0,20):
        accepts = []
        for j in range(0,HIRE_POOL):
            if potential_hires[j].accept_offer(bus.offer):
                accepts.append(potential_hires[j])
        bus.update_employees(accepts)
        bus.update_offer()
    return bus, potential_hires, num_strat

def run_trial2(number_optimized):
    bus, potential_hires, num_strat = init_trial2(number_optimized)
    for i in range(0,20):
        accepts = []
        for j in range(0,HIRE_POOL):
            if potential_hires[j].accept_offer(bus.offer):
                accepts.append(potential_hires[j])
        bus.update_employees(accepts)
        bus.update_offer()
    return bus, potential_hires, num_strat

def gather_stats(potential_hires, num_strat):
    offers = []
    amount_won = [0] * len(stratClasses)
    for i in range(0,HIRE_POOL):
        offers.append(potential_hires[i].accept_amount)
        if potential_hires[i].hired:
            for j in range(0,len(stratClasses)):
                if type(potential_hires[i]) == stratClasses[j]:
                    amount_won[j] = amount_won[j] + potential_hires[i].accept_amount

    #print("num empoyees: ", bus.get_num_employees())
    for i in range(0,len(stratClasses)):
        if num_strat[i] is not 0:
            amount_won[i] = amount_won[i] / num_strat[i]
        else:
            amount_won[i] = 0

    return amount_won

def main():
    avg_amount_won = [0] * len(stratClasses)
    

    for i in range(0, NUM_TRIALS):
        bus, potential_hires, num_strat = run_trial()
        amount_won = gather_stats(potential_hires, num_strat)
        for j in range(0, len(stratClasses)):
            avg_amount_won[j] = avg_amount_won[j] + amount_won[j]

    for i in range(0,len(stratClasses)):
        avg_amount_won[i] = avg_amount_won[i] / NUM_TRIALS
        print(stratClasses[i].strategy, " earnings: ", avg_amount_won[i])

    total_avg = 0
    for i in range(0,len(stratClasses)):
        total_avg = total_avg + avg_amount_won[i]

    total_avg = total_avg / (len(stratClasses))
    #total_avg = total_avg * (1 - number_balanced / HIRE_POOL) + avg_amount_won[3] * (number_balanced / HIRE_POOL)


    variance = 0
    for i in range(0, len(stratClasses)):
        variance = variance + (avg_amount_won[i] - total_avg)**2

    variance = variance  / (len(stratClasses))
    #variance = variance * (1 - number_balanced / HIRE_POOL) + ((avg_amount_won[3] - total_avg)**2) * (number_balanced / HIRE_POOL)

    std_dev = math.sqrt(variance)
    print("Average earnings: ", total_avg)
    print("Variance: ", variance)


    strats = []
    for i in range(0,len(stratClasses)):
        strats.append(stratClasses[i].strategy)

    x = range(0,len(stratClasses))
    fig, ax = plt.subplots()
    rects = ax.bar(x, avg_amount_won, 0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(strats)

    fig.tight_layout()

    plt.title("Strategies Performance at 20% Hire Rate")
    plt.ylabel("Average Money Earned")

    plt.show()

main()
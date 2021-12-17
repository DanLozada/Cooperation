#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 6.

Comment: 7/10 
The graph is incorrect. 
First, you will need to merge all 3 plots into one single mesh in order to see the differences between scenarios. 
Note that, in case of having a few strong cooperators in the set, you should expect to see the curve much smoother than the other two. 

Please check the sample solution. But be careful that you need to change the inputs in the sample solution for the last 2 scenarios to 5 and 25 instead of 2 and 28. 
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from pprint import pprint

random.seed(380)

# =============================================================================
# Section 1. Define classes
# =============================================================================
# 1.1. Define a class "Player". For the player class


class Player:
    def __init__(self, winnings=0, endowment=100):
        self.endowment = endowment
        self.winnings = winnings

    def self_introduction(self):
        print(f'I have {self.endowment} in my endowment')

    def contribute(self):
        contribution = self.endowment * random.randint()
        self.winnings += self.endowment - contribution
        return contribution

    def record_winnings(self, pot_winnings):
        self.winnings += pot_winnings


# 1.2. Define "Free_rider" as a child class of "Player"
class Free_rider(Player):
    def __init__(self, endowment=100, winnings=0, type='free-rider'):
        super().__init__(endowment, winnings)
        self.type = type

    def contribute(self):
        randomness = random.randint(0, 1)
        if randomness < 0.5:
            contribution = self.endowment * random.randint(0, 1)
        else:
            contribution = 0
        # whatever is not contributed is considered winnings
        self.winnings += self.endowment - contribution
        return contribution

# 1.3. Define "Strong_cooperator" as a child class of "Player"


class Strong_cooperator(Player):
    def __init__(self, endowment=100, winnings=0, type='strong'):
        super().__init__(endowment, winnings)
        self.type = type

    def contribute(self):
        return self.endowment

# 1.4. Define "Conditional_cooperator" as a child class of "Player"


class Conditional_cooperator(Player):
    def __init__(self, endowment=100, winnings=0, type='conditional'):
        super().__init__(endowment, winnings)
        self.type = type

    def contribute(self, previous_round_average_contribution):
        if previous_round_average_contribution:
            contribution = 0.8 * previous_round_average_contribution
        else:
            contribution = self.endowment * random.randint(0, 1)
        self.winnings += self.endowment - contribution
        return contribution

# =============================================================================
# Section 2. Simulating Social Interaction
# =============================================================================


def experiment(society, num_periods=20):
    total_contributions = []
    avg_contributions = [100]

    for round in range(num_periods):
        total_contribution = 0

        for individual in society:
            if individual.type == 'conditional':
                total_contribution += individual.contribute(
                    avg_contributions[round])
            else:
                total_contribution += individual.contribute()

        average_for_round = total_contribution / len(society)
        avg_contributions.append(average_for_round)
        total_contributions.append(total_contribution)

        for individual in society:
            individual.winnings += average_for_round * 2

        print(
            f"In round {round+1}, total contribution was {total_contribution}")

    return total_contributions, avg_contributions


# 2.1. Scenario One. Interaction among conditional Cooperators
conditional_cooperators_1 = [Conditional_cooperator() for i in range(31)]
society_1 = conditional_cooperators_1
total_contribution_1, avg_contributions_1 = experiment(society_1)

# 2.2. Scenario Two. Interaction with free riders
free_riders_2 = [Free_rider() for i in range(6)]
conditional_cooperators_2 = [Conditional_cooperator() for i in range(26)]
society_2 = conditional_cooperators_2 + free_riders_2
total_contribution_2, avg_contributions_2 = experiment(society_2)

# 2.3. Scenario Three. Different starting point.
strong_cooperators_3 = [Strong_cooperator() for i in range(5)]
conditional_cooperators_3 = [Conditional_cooperator() for i in range(26)]
society_3 = conditional_cooperators_3 + strong_cooperators_3
total_contribution_3, avg_contributions_3 = experiment(society_3)

# =============================================================================
# Section 3. Result visualization and interpretation
# =============================================================================
# 3.1 visualize the simulation results by ploting the average contribution
# overtime (Three scenarios on the same figure).


def plot_avg_contributions(outcome1, outcome2, outcome3):
    plt.style.use('seaborn')
    fig = plt.figure(figsize=(20, 10))

    ax = fig.add_subplot(311)
    bx = fig.add_subplot(312)
    cx = fig.add_subplot(313)

    rounds = np.linspace(1, 21, 21)

    ax.set_title('Society 1')
    ax.plot(rounds, outcome1, 'b', label='Society 1')
    bx.set_title('Society 2')
    bx.plot(rounds, outcome2, 'g', label='Society 2')
    cx.set_title('Society 3')
    cx.plot(rounds, outcome3, 'r', label='Society 3')

    plt.suptitle('Agent-based Modeling Matching Fund Game', fontsize=20)
    plt.show()


plot_avg_contributions(avg_contributions_1,
                       avg_contributions_2, avg_contributions_3)


# Helper functions for 3.2 and 3.3

def add_elements(list, total=0):
    for i in list:
        total += i
    return total


def compare_scenarios(total_contributions_1, total_contributions_2):
    # add all of the values inside each scenarios total welfare
    total_1 = add_elements(total_contributions_1)
    total_2 = add_elements(total_contributions_2)
    # get percent change of between scenario_1 and scenario_2
    return ((total_1 - total_2) / total_1) * 100


def total_earnings(my_list):
    running_count = 0
    for individual in my_list:
        running_count += individual.winnings
    return running_count


def compare_total_earnings(my_dict):
    current_highest = ''
    current_highest_amount = 0
    current_lowest = ''
    current_lowest_amount = 10000000000  # Some huge number
    for i in my_dict.keys():
        if my_dict[i] > current_highest_amount:
            current_highest_amount = my_dict[i]
            current_highest = i
        if my_dict[i] < current_lowest_amount:
            current_lowest_amount = my_dict[i]
            current_lowest = i

    return current_highest, current_highest_amount, current_lowest, current_lowest_amount


"""
3.2. Compare the results of Scenario 2 to Scenario 1, what is the net loss in
total social welfare (percentage change)?
"""

print('Comparison of Society 1 and 2')

pct_change_total_contributions_1_vs_2 = compare_scenarios(
    total_contribution_1, total_contribution_2)
print(
    f"The percent change in total contributions is {pct_change_total_contributions_1_vs_2}%")

earnings_cc_1 = total_earnings(conditional_cooperators_1)
earnings_cc_2 = total_earnings(conditional_cooperators_2)
earnings_fr_2 = total_earnings(free_riders_2)

comparison_1 = {
    # 'cc_1': earnings_cc_1,
    'cc_2': earnings_cc_2,
    'fr_2': earnings_fr_2
}

highest, highest_amount, lowest, lowest_amount = compare_total_earnings(
    comparison_1)

print(
    f"In comparing society 1 and 2, the highest earner is {highest} with {highest_amount} and the lowest earner is {lowest} with {lowest_amount}")

"""
3.3. Compare the results of Scenario 3 to Scenario 1, what is the net gain in
total social welfare (percentage change)?
"""
print('----------------------------------------------------------------')


print('Comparison of Society 1 and 3')

pct_change_total_contributions_1_vs_3 = compare_scenarios(
    total_contribution_1, total_contribution_3)
print(
    f"The percent change in total contributions is {pct_change_total_contributions_1_vs_3}%")


earnings_cc_3 = total_earnings(conditional_cooperators_3)
earnings_sc_3 = total_earnings(strong_cooperators_3)

comparison_2 = {
    # 'cc_1': earnings_cc_1,
    'cc_3': earnings_cc_3,
    'sc_3': earnings_sc_3
}

highest, highest_amount, lowest, lowest_amount = compare_total_earnings(
    comparison_2)

print(
    f"In comparing society 1 and 3, the highest earner is {highest} with {highest_amount} and the lowest earner is {lowest} with {lowest_amount}")

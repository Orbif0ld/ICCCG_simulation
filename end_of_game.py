import random
import matplotlib.pyplot as plt
from math import sqrt


def judge(p):
    """select correct answer with probability p
    returns 0 for incorrect, 1 for correct judgement"""
    return 0 if random.uniform(0, 1) > p else 1


def play_game(num_rounds, p_judge):
    """estimate p from num_rounds rounds of the game"""
    p_correct_estimate = sum([judge(p_judge)
                              for i in range(num_rounds)]) / num_rounds
    return p_correct_estimate


def play_many_games(num_games, num_rounds, p_judge):
    """returns  a list of estimated ps from num_games games"""
    estimated_distribution = [
        play_game(num_rounds, p_judge) for i in range(num_games)]
    return estimated_distribution


def empirical_variance(sample):
    """sample:  list of values for p"""
    n = len(sample)
    mean = sum(sample) / n
    var = sum([(s - mean)**2 for s in sample]) / (n - 1)
    return var


def empirical_standard_deviation(sample):
    return sqrt(empirical_variance(sample))


plt.figure(1)

distrs = [(play_many_games(1000, 100, i / 10), i / 10) for i in range(5, 10)]

[plt.hist(dist, label=str(p), normed=True) for dist, p in distrs]
plt.legend()
plt.title(r"distributions of $p_{estimated}$ for different $p$")

plt.figure(2)

distrs = [(play_many_games(1000, 10, i / 100), i / 100)
          for i in range(50, 100)]
emp_std = [(empirical_standard_deviation(distr), p) for distr, p in distrs]
stds, probs = zip(*emp_std)

plt.plot(probs, stds)
plt.title(r"standard deviation as a function of $p_{correct}$")

plt.show()

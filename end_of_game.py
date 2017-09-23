import random
import matplotlib.pyplot as plt
from math import sqrt


# the model:
# * at each point in time the guesser possesses a certain fraction f
#   of the information contained in the document.
# * the probability that the judge correctly identifies the guesser's answer
#   is p = 1 when f = 0 and p = 0.5 when f = 1. (e.g. p = 1 - f/2)
#   the point is that it is possible to infer f from p.
# * p is estimated using p = #correct_judgementes/#judgements
#   (maximum likelihood estimator for bernoulli random variable)
# * the game should end when the guesser reaches f close to 1
#   <=> the judge reaches p close to 0.5.
# * for simplicity in this simulation f and p do not change across multiple
#   rounds. the result is therefor a lower bound on the standard deviation.
#
# validity:
# the model is very simple and does not really account for intelligent
# players. for example, if the reader systematically asks hard to guess
# questions until he/she runs out of new things to ask, the judge's
# performance will probably be consistently high at first until it suddenly
# falls off a cliff. that cliff would be easy to detect.
# however that sort of thing depends on the reader's efficiency and also
# on who gets to ask the questions (which is random atm).
#
# results:
# I ran the code below with several different parameters.
# for num_rounds = 30 the standard deviation is close to 0.1 for
# p close to 0.5. for num_rounds = 3 the standard deviation is close
# to 0.3.
#
# conclusion:
# a good method for determining the end of the game automatically
# would probably require inspection of the data that the game generates.
# (maybe it will turn out that the "falling off a cliff" behavior is
# typical.) until such data is available, IMO human players should be able to
# determine themselves when the game should end - the reader will eventually
# be acutely aware that they do not have anything new to ask, anyway. if
# there is no way out, players might be compelled to start asking questions
# like "what's the 25th letter in the document", but that does not seem
# desirable.

num_games = 1000
num_rounds = 3


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

distrs = [(play_many_games(num_games, num_rounds, i / 10), i / 10)
          for i in range(5, 10)]

[plt.hist(dist, label=str(p), normed=True) for dist, p in distrs]
plt.legend()
plt.title(r"distributions of $p_{estimated}$ for different $p$")

plt.figure(2)

distrs = [(play_many_games(num_games, num_rounds, i / 100), i / 100)
          for i in range(50, 100)]
emp_std = [(empirical_standard_deviation(distr), p) for distr, p in distrs]
stds, probs = zip(*emp_std)

plt.plot(probs, stds)
plt.title(r"standard deviation as a function of $p_{correct}$")

plt.show()

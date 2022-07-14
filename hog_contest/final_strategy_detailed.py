"""
    This file contains your final_strategy that will be submitted to the contest.

    You can only depend on "general-purpose" libraries - do not import or open any
    contest-specific files, like other Python or text files. All contest logic must
    be in this file.

    Remember to supply a unique PLAYER_NAME or your submission will not succeed.
"""

PLAYER_NAME = 'λ'  # Change this line!

GOAL_SELF = 50
GOAL_OPP = 65

def final_strategy(score, opp_score):
    """ Returns the optimal roll that provides best probability of winning

    Args:
        score: score of current player
        opp_score: opponent score
    
    Returns:
        An integer representing the optimal number of rolls
    """
    if score == 0 and opp_score == 0: return 0
    roll_prob_arr = [prob_win_by_roll_num(score, opp_score, rn) for rn in range(11)]
    return max(range(11), key = lambda ind: roll_prob_arr[ind])
    
#SECTION 1: Operation Utility

f_a_log = {}
def memoized(func):
    """Memoizes function operations"""
    def lookup(*args):
        keys = (func, args)
        if keys not in f_a_log:
            f_a_log[keys] = func(*args)
        return f_a_log.get(keys)
    return lookup

def scoring_from_zero(score, opp_score):
    """Returns the score attained by rolling zero dices.

    Args:
        score: score of current player
        opp_score: score of opponent

    Returns:
        An integer representing the number of points got by rolling zero dices.
    """
    increment = [7, 1, 4, 2, 8, 5][opp_score % 6]
    return increment + int(score + increment == opp_score) * opp_score

#SECTION 2: Dices and Probabilities

@memoized
def probability_with_roll(target, roll_num):
    """Returns probability of getting TARGET with ROLL_NUM rolls with probability function P.
    
    Args:
        target: Target score
        roll_num: Target number of rolls
    
    Returns:
        A floating-point representing the probability to get TARGET with ROLL_NUM rolls 
        given probability function P
    """
    assert target > 0, 'target is less than or equal to 0'
    assert roll_num > 0, 'roll_num is less than or equal to 0'
    if target == 1: return probability_one(roll_num)
    return probability_none_one(target, roll_num)

@memoized
def probability_one(roll_num):
    """Returns probability of scoring 1 in ROLL_NUM rolls.
    
    Args:
        roll_num: Target number of rolls
    
    Returns:
    A floating-point representing the probability that player scores 1.
    """
    assert roll_num > 0, 'roll_num is less than or equal to 0'
    return 1/6 if roll_num == 1 else 1/6 + 5/6 * probability_one(roll_num - 1)

@memoized
def probability_none_one(total_score, roll_num):
    """Returns probability of scoring TOTAL_SCORE in ROLL_NUM rolls.
    
    Args:
        roll_num: Target number of rolls
    
    Returns:
        A floating-point representing the aforementioned probability.
    """
    if total_score == 0 and roll_num == 0: return 1
    if roll_num == 0: return 0
    total_probability = 0
    for i in range(2, 7):
        total_probability += 1/6 * probability_none_one(total_score - i, roll_num - 1)
    return total_probability

@memoized
def probability_at_least_score(minimum, roll_num):
    """Returns probability of scoring at least MINIMUM in ROLL_NUM rolls.
    
    Args:
        minimum: The lower bound of desired score
        roll_num: Target number of rolls
    
    Returns:
        A floating-point representing the aforementioned probability.
    """
    total_probability = 0
    for s in range(minimum, roll_num * 6 + 1):
        total_probability += probability_with_roll(s, roll_num)
    assert total_probability > 1, f'total probability is {total_probability} > 1'
    return total_probability

'''
@memoized
def optimal_rolls(minimum, score, opp_score):
    """Returns the optimal number of rolls to get at least MINIMUM.

    Args:
        minimum: the minimum target score desired.
        score: current player's scores
        opp_score: opponent's scores
    
    Returns:
        Integer representing number of rolls that most possibly score at least MINIMUM.
    """
    roll_num_probability_arr = [probability_at_least_score(minimum, rn) for rn in range(1, 11)]
    without_rules = max(range(1, 11), key = lambda ind: roll_num_probability_arr[ind - 1])
    return 0 if scoring_from_zero(score, opp_score) >= minimum else without_rules
'''

#SECTION 3: Probability

@memoized
def prob_win_by_roll_num(score, opp_score, roll_num):
    """ Probability to win by rolling roll_num times.

    Args:
        score: current player's score
        opp_score: opponent's score
        roll_num: the amount of times dice is rolled this time
    Returns:
        A floating-point number representing the aforemtioned probability.
    """
    total_probability = 0
    if roll_num == 0: 
        return prob_win_by_pts(score + scoring_from_zero(score, opp_score), opp_score)
    for pts in range(1, 6 * roll_num + 1):
        total_probability += probability_with_roll(pts, roll_num) * prob_win_by_pts(score + pts, opp_score)
    return total_probability

@memoized
def prob_win_by_pts(score, opp_score):
    """ Probability of winning given a current scoring.

    Args:
        score: current player's scores
        opp_score: opponent's scores
    Returns:
        A floating-point number representing the aforemtioned probability.
    """
    if score >= GOAL_SELF: return 1
    if opp_score >= GOAL_OPP: return 0
    opp_win = prob_win_by_roll_num(opp_score, score, final_strategy(opp_score, score))
    return 1 - opp_win

#SECTION 4: Looping Tests

#'''
import time
start = time.time()
for i in range(300):
    for j in range(300):
        final_strategy(i, j)
print("DEBUG:", f'time is {time.time() - start} seconds')
#'''
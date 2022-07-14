PLAYER_NAME, GOAL_SELF, GOAL_OPP, f_a_log = "[ 謎の ■■■■■ λ ]", 50, 50, {}

def final_strategy(score, opp_score):
    if score + opp_score == 0: return 0
    roll_prob_arr = [prob_win_by_r_n(score, opp_score, rn) for rn in range(11)]
    return max(range(11), key = lambda ind: roll_prob_arr[ind])

def memoized(func):
    def lookup(*args):
        keys = (func, args)
        if keys not in f_a_log: f_a_log[keys] = func(*args)
        return f_a_log.get(keys)
    return lookup

def scoring_from_zero(score, opp_score):
    inc = [7, 1, 4, 2, 8, 5][opp_score % 6]
    return inc + int(score + inc == opp_score) * opp_score

@memoized
def prob_with_roll(target, r_n):
    return prob_one(r_n) if target == 1 else prob_none_one(target, r_n)

@memoized
def prob_one(r_n):
    return 1/6 if r_n == 1 else 1/6 + 5/6 * prob_one(r_n - 1)

@memoized
def prob_none_one(total, r_n):
    if total == 0 and r_n == 0: return 1
    if r_n == 0: return 0
    return sum([1/6 * prob_none_one(total - i, r_n - 1) for i in range(2, 7)])

@memoized
def prob_win_by_r_n(score, opp_score, r_n):
    if r_n == 0: 
        return prob_win_by_pts(score + scoring_from_zero(score, opp_score), opp_score)
    return sum([prob_with_roll(pts, r_n) * prob_win_by_pts(score + pts, opp_score)
                for pts in range(1, 6 * r_n + 1)])

@memoized
def prob_win_by_pts(score, opp_score):
    if score >= GOAL_SELF: return 1
    if opp_score >= GOAL_OPP: return 0
    return 1 - prob_win_by_r_n(opp_score, score, final_strategy(opp_score, score))

"""
Bull Put Spread Strategy

This strategy consists of two Put options:
Selling High Strike Put and Buying Lower Strike Put
"""

import numpy as np
from scipy.stats import norm as nd
import option_pricing_black_scholes as opbs

def payoff(S0, Klp, Ksp, DTE0, IV0, r, strike_list, rng_stock):
    CONTRACT = 1    # number of options contract
    MULTI = 100     # options multiplier
    STEP = 0.50     # step for stock price for the payoff calculation

    # option pricing params (S, K, DTE, IV%, r%)
    # entry day index '0'
    long_put_params0 = (S0, Klp, DTE0, IV0, r)
    short_put_params0 = (S0, Ksp, DTE0, IV0, r)

    # Long / Short Put price calculation
    # lp0: long put price
    # sp0: short put price
    objlp = opbs.OptionPricing(*long_put_params0)
    objsp = opbs.OptionPricing(*short_put_params0)
    lp0 = objlp.price()["put"]
    sp0 = objsp.price()["put"]

    # Stock price range from the min/max strike price
    DISTANCE_FROM_STRIKE = rng_stock
    stock_price_arr = np.arange(long_put_params0[1] - DISTANCE_FROM_STRIKE,
                                short_put_params0[1] + DISTANCE_FROM_STRIKE
                                + STEP, STEP)
    # Break Even Point
    bep = round(Ksp - sp0 + lp0,2)

    payoff_list = []
    # THE RESULT FUNCTION (PAYOFF) @ EXPIRATION
    for i in stock_price_arr:
        if i <= Klp:
            res_at_expiration = (Klp - bep)
        elif Klp < i < Ksp:
            res_at_expiration = (i - bep)
        elif i >= Ksp:
            res_at_expiration = (sp0 - lp0)

        payoff_at_exp = res_at_expiration * MULTI * CONTRACT
        payoff_list.append(payoff_at_exp)

    payoff_arr=np.array(payoff_list).T

    return sp0, lp0, bep, stock_price_arr, payoff_arr

def prob_calc(S0, sp0, lp0, bep, Klp, Ksp, DTE0, IV0):

    # Period Volatility
    period_vol = IV0 / 100 * np.sqrt(DTE0 / 365)

    # z-values
    z0 = -4
    z1 = np.log(Klp / S0) / period_vol
    z2 = np.log(bep / S0) / period_vol
    z3 = np.log(Ksp / S0) / period_vol
    z4 = 4

    # Probability
    PR01 = nd.cdf(z1) - nd.cdf(z0)
    PR12 = nd.cdf(z2) - nd.cdf(z1)
    PR23 = nd.cdf(z3) - nd.cdf(z2)
    PR34 = nd.cdf(z4) - nd.cdf(z3)

    PR_list = [PR01, PR12, PR23, PR34]

    # Nx01 = None
    Nx12 = nd.cdf(z2 - period_vol) - nd.cdf(z1 - period_vol)
    Nx23 = nd.cdf(z3 - period_vol) - nd.cdf(z2 - period_vol)
    # Nx34 = nd.cdf(z4 - period_vol) - nd.cdf(z3 - period_vol)

    # Expected Value
    ER1 = (Klp - bep) * PR01
    ER2 = S0 * np.exp(period_vol**2 / 2) * Nx12 - bep * PR12
    ER3 = S0 * np.exp(period_vol**2 / 2) * Nx23 - bep * PR23
    ER4 = (sp0 - lp0) * PR34

    ER_list = [ER1, ER2, ER3, ER4]
    # Expected Result
    ER = round(sum(ER_list),3)

    # Collects Expected Results and Probabilities Values
    ER_PR_arr = np.array([ER_list, PR_list])

    PR_pos_list = [ER_PR_arr[1][i] for i, ER in enumerate(ER_PR_arr[0]) if ER > 0]
    # PR_neg_list = [ER_PR_arr[1][i] for i, ER in enumerate(ER_PR_arr[0]) if ER <= 0]

    # Probability of Gain / Loss
    PR_gain = round(sum(PR_pos_list),3)
    PR_loss = round(1 - PR_gain,3)

    maxGain = round(sp0 - lp0,2)
    maxLoss = round(Klp - bep,2)

    res_row = [Klp, lp0, Ksp, sp0, bep, PR_gain, PR_loss, maxGain, maxLoss, ER]
    return res_row

def run_strategy(S0, Klp, Ksp, DTE0, IV0, r, selected, strike_list, rng_stock):
    # If 'selected' is False the script is looking for all available trades
    # Results of each trade are collected in 'res_row'
    if selected == False:
        sp0, lp0, bep, stock_price_arr, payoff_arr = payoff(S0, Klp, Ksp, DTE0,
                                                            IV0, r, strike_list, rng_stock)
        res_row = prob_calc(S0, sp0, lp0, bep, Klp, Ksp, DTE0, IV0)
        return res_row

    # If 'selected' is True, the best strategy (the largest ER) is found
    # and ready for charting
    # Data for payoff diagram is collected in 'chart_data'
    elif selected == True:
        sp0, lp0, bep, stock_price_arr, payoff_arr = payoff(S0, Klp, Ksp, DTE0,
                                                            IV0, r, strike_list, rng_stock)
        chart_data = [stock_price_arr, payoff_arr]
        return chart_data

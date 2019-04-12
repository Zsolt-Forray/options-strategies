"""
Bull Call Spread Strategy

This strategy consists of two call options:
Selling High Strike Call and Buying Lower Strike Call
"""

import numpy as np
from scipy.stats import norm as nd
import option_pricing_black_scholes as opbs

def payoff(S0, Ksc, Klc, DTE0, IV0, r, strike_list, rng_stock):
    CONTRACT = 1    # number of options contract
    MULTI = 100     # options multiplier
    STEP = 0.50     # step for stock price for the payoff calculation

    # option pricing params (S, K, DTE, IV%, r%)
    # entry day index '0'
    long_call_params0 = (S0, Klc, DTE0, IV0, r)
    short_call_params0 = (S0, Ksc, DTE0, IV0, r)

    # Long / Short Call price calculation
    # lc0: long call price
    # sc0: short call price
    lc0 = round(opbs.OptionPricing(*long_call_params0).call_price(),2)
    sc0 = round(opbs.OptionPricing(*short_call_params0).call_price(),2)

    # Stock price range from the min/max strike price
    DISTANCE_FROM_STRIKE = rng_stock
    stock_price_arr = np.arange(long_call_params0[1] - DISTANCE_FROM_STRIKE,
                                short_call_params0[1] + DISTANCE_FROM_STRIKE
                                + STEP, STEP)
    # Break Even Point
    bep = round(Klc - sc0 + lc0,2)

    payoff_list = []
    # THE RESULT FUNCTION (PAYOFF) @ EXPIRATION
    for i in stock_price_arr:
        if i <= Klc:
            res_at_expiration = (sc0 - lc0)
        elif Klc < i < Ksc:
            res_at_expiration = (i - bep)
        elif i >= Ksc:
            res_at_expiration = (Ksc - bep)

        payoff_at_exp = res_at_expiration * MULTI * CONTRACT
        payoff_list.append(payoff_at_exp)

    payoff_arr=np.array(payoff_list).T

    return sc0, lc0, bep, stock_price_arr, payoff_arr

def prob_calc(S0, sc0, lc0, bep, Ksc, Klc, DTE0, IV0):

    # Period Volatility
    period_vol = IV0 / 100 * np.sqrt(DTE0 / 365)

    # z-values
    z0 = -4
    z1 = np.log(Klc / S0) / period_vol
    z2 = np.log(bep / S0) / period_vol
    z3 = np.log(Ksc / S0) / period_vol
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
    ER1 = (sc0 - lc0) * PR01
    ER2 = S0 * np.exp(period_vol**2 / 2) * Nx12 - bep * PR12
    ER3 = S0 * np.exp(period_vol**2 / 2) * Nx23 - bep * PR23
    ER4 = (Ksc - bep) * PR34

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

    maxGain = round(Ksc - bep,2)
    maxLoss = round(sc0 - lc0,2)

    res_row = [Klc, lc0, Ksc, sc0, bep, PR_gain, PR_loss, maxGain, maxLoss, ER]
    return res_row

def run_strategy(S0, Klc, Ksc, DTE0, IV0, r, selected, strike_list, rng_stock):
    # If 'selected' is False the script is looking for all available trades
    # Results of each trade are collected in 'res_row'
    if selected == False:
        sc0, lc0, bep, stock_price_arr, payoff_arr = payoff(S0, Ksc, Klc, DTE0,
                                                            IV0, r, strike_list, rng_stock)
        res_row = prob_calc(S0, sc0, lc0, bep, Ksc, Klc, DTE0, IV0)
        return res_row

    # If 'selected' is True, the best strategy (the largest ER) is found
    # and ready for charting
    # Data for payoff diagram is collected in 'chart_data'
    elif selected == True:
        sc0, lc0, bep, stock_price_arr, payoff_arr = payoff(S0, Ksc, Klc, DTE0,
                                                            IV0, r, strike_list, rng_stock)
        chart_data = [stock_price_arr, payoff_arr]
        return chart_data

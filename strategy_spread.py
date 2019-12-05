#!/usr/bin/python3


"""
Bull Call Spread Strategy:
- This strategy consists of two call options:
- Selling High Strike Call and Buying Lower Strike Call

Bull Put Spread Strategy
- This strategy consists of two Put options:
- Selling High Strike Put and Buying Lower Strike Put
"""


__author__  = 'Zsolt Forray'
__license__ = 'MIT'
__version__ = '0.0.1'
__date__    = '05/12/2019'
__status__  = 'Development'


import numpy as np
import option_pricing_black_scholes as bs
from probability_calc import Probability


class Spread:
    """
    General/Main class for options spread strategy calculation.
    """
    def __init__(self, S, low_K, high_K, DTE, IV, rate, strategy):
        self.S      = S
        self.low_K  = low_K
        self.high_K = high_K
        self.DTE    = DTE
        self.IV     = IV
        self.rate   = rate
        self.strategy = strategy

    def calc_stock_price_arr(self):
        RNG_STOCK = 15          # Stock price range from the min/max strike price
        STOCK_PRICE_STEP = 0.5  # step for stock price for the payoff calculation
        DISTANCE_FROM_STRIKE = RNG_STOCK
        self.stock_price_arr = np.arange(max(self.low_K - DISTANCE_FROM_STRIKE,0),
                                         self.high_K + DISTANCE_FROM_STRIKE
                                         + STOCK_PRICE_STEP, STOCK_PRICE_STEP)

    def calc_option_price(self):
        price_obj = Price(self.S, self.low_K, self.high_K, self.DTE, self.IV,\
                          self.rate, self.strategy)
        self.low_price, self.high_price = price_obj.run_price()

    def calc_break_even_point(self):
        bep_obj = BreakEvenPoint(self.high_K, self.low_K,\
                                 self.high_price, self.low_price, self.strategy)
        self.bep = bep_obj.run_bep()

    def calc_payoff(self):
        pay_obj = Payoff(self.stock_price_arr, self.low_K, self.high_K, self.bep,\
                         self.high_price, self.low_price, self.strategy)
        self.payoff_arr =  pay_obj.run_payoff()

    def run_strategy(self):
        self.calc_stock_price_arr()
        self.calc_option_price()
        self.calc_break_even_point()
        self.calc_payoff()
        prob_obj = Probability(self.S, self.high_price, self.low_price, self.bep,\
                               self.high_K, self.low_K, self.DTE, self.IV, self.strategy)
        return prob_obj.run_probability()

    def collect_chart_data(self):
        self.calc_stock_price_arr()
        self.calc_option_price()
        self.calc_break_even_point()
        self.calc_payoff()
        return self.stock_price_arr, self.payoff_arr


class Price:
    """
    Calculates Call/Put options price based on the selected spread strategy.
    """
    def __init__(self, S, low_K, high_K, DTE, IV, rate, strategy):
        self.S = S
        self.low_K = low_K
        self.high_K = high_K
        self.DTE = DTE
        self.IV = IV
        self.rate = rate
        self.strategy = strategy

    def run_price(self):
        strategies = \
        {
            "bull_call_spread"  : lambda : Price.bull_call_prices(self.S, self.low_K,\
                                           self.high_K, self.DTE, self.IV, self.rate),
            "bull_put_spread"   : lambda : Price.bull_put_prices(self.S, self.low_K,\
                                           self.high_K, self.DTE, self.IV, self.rate),
        }
        return strategies[self.strategy]()

    @staticmethod
    def bull_call_prices(S, low_K, high_K, DTE, IV, rate):
        price_obj = bs.OptionPrice(S, low_K, DTE, IV, rate)
        low_price = price_obj.call_price()
        price_obj = bs.OptionPrice(S, high_K, DTE, IV, rate)
        high_price = price_obj.call_price()
        return low_price, high_price

    @staticmethod
    def bull_put_prices(S, low_K, high_K, DTE, IV, rate):
        price_obj = bs.OptionPrice(S, low_K, DTE, IV, rate)
        low_price = price_obj.put_price()
        price_obj = bs.OptionPrice(S, high_K, DTE, IV, rate)
        high_price = price_obj.put_price()
        return low_price, high_price


class BreakEvenPoint:
    """
    Calculates the Break Even Point based on the selected spread strategy.
    """
    def __init__(self, high_K, low_K, high_price, low_price, strategy):
        self.high_K = high_K
        self.low_K = low_K
        self.high_price = high_price
        self.low_price = low_price
        self.strategy = strategy

    def run_bep(self):
        strategies = \
        {
        "bull_call_spread"  : \
        lambda : BreakEvenPoint.bull_call_bep(self.low_K, self.high_price, self.low_price),
        "bull_put_spread"   : \
        lambda : BreakEvenPoint.bull_put_bep(self.high_K, self.high_price, self.low_price),
        }
        return strategies[self.strategy]()

    @staticmethod
    def bull_call_bep(low_K, high_price, low_price):
        return round(low_K - high_price + low_price, 2)

    @staticmethod
    def bull_put_bep(high_K, high_price, low_price):
        return round(high_K - high_price + low_price, 2)


class Payoff:
    """
    Calculates the Result Function (Payoff) @ EXPIRATION
    based on the selected spread strategy.
    """
    MULTI = 100     # options multiplier
    CONTRACT = 1    # number of options contract
    def __init__(self, stock_price_arr, low_K, high_K, bep,\
                 high_price, low_price, strategy):
        self.stock_price_arr = stock_price_arr
        self.low_K = low_K
        self.high_K = high_K
        self.bep = bep
        self.high_price = high_price
        self.low_price = low_price
        self.strategy = strategy

    def run_payoff(self):
        strategies = \
        {
            "bull_call_spread"  : \
            lambda : Payoff.bull_call_payoff(self.stock_price_arr, self.high_K, self.low_K,\
                                             self.bep, self.high_price, self.low_price),
            "bull_put_spread"   : \
            lambda : Payoff.bull_put_payoff(self.stock_price_arr, self.high_K, self.low_K,\
                                            self.bep, self.high_price, self.low_price),
        }
        return strategies[self.strategy]()

    @staticmethod
    def bull_call_payoff(stock_price_arr, high_K, low_K, bep, high_price, low_price):
        payoff_list = []
        for i in stock_price_arr:
            if i <= low_K:
                res_at_expiration = (high_price - low_price)
            elif low_K < i < high_K:
                res_at_expiration = (i - bep)
            elif i >= high_K:
                res_at_expiration = (high_K - bep)
            payoff_at_exp = res_at_expiration * Payoff.MULTI * Payoff.CONTRACT
            payoff_list.append(payoff_at_exp)
        payoff_arr = np.array(payoff_list).T
        return payoff_arr

    @staticmethod
    def bull_put_payoff(stock_price_arr, high_K, low_K, bep, high_price, low_price):
        payoff_list = []
        for i in stock_price_arr:
            if i <= low_K:
                res_at_expiration = (low_K - bep)
            elif low_K < i < high_K:
                res_at_expiration = (i - bep)
            elif i >= high_K:
                res_at_expiration = (high_price - low_price)
            payoff_at_exp = res_at_expiration * Payoff.MULTI * Payoff.CONTRACT
            payoff_list.append(payoff_at_exp)
        payoff_arr = np.array(payoff_list).T
        return payoff_arr

#!/usr/bin/python3


"""
Probability calculator
"""


__author__  = 'Zsolt Forray'
__license__ = 'MIT'
__version__ = '0.0.1'
__date__    = '05/12/2019'
__status__  = 'Development'


import numpy as np
from scipy.stats import norm as nd


class Probability:
    """
    General/Main class for Probability & Expected Result calculations.
    """
    def __init__(self, S, high_opt_price, low_opt_price, bep, high_K, low_K,\
                 DTE, IV, strategy):
        self.S = S
        self.high_price = high_opt_price
        self.low_price = low_opt_price
        self.bep = bep
        self.high_K = high_K
        self.low_K = low_K
        self.DTE = DTE
        self.IV = IV
        self.strategy = strategy

    def calc_period_volatility(self):
        # Period Volatility
        self.period_vol = self.IV / 100 * np.sqrt(self.DTE / 365)

    def calc_z_values(self):
        # z-values
        z0 = -4
        z1 = np.log(self.low_K / self.S) / self.period_vol
        z2 = np.log(self.bep / self.S) / self.period_vol
        z3 = np.log(self.high_K / self.S) / self.period_vol
        z4 = 4
        self.z_list = [z0, z1, z2, z3, z4]

    def calc_sections_probability(self):
        # Sections probability
        PR01 = nd.cdf(self.z_list[1]) - nd.cdf(self.z_list[0])
        PR12 = nd.cdf(self.z_list[2]) - nd.cdf(self.z_list[1])
        PR23 = nd.cdf(self.z_list[3]) - nd.cdf(self.z_list[2])
        PR34 = nd.cdf(self.z_list[4]) - nd.cdf(self.z_list[3])
        self.PR_list = [PR01, PR12, PR23, PR34]

    def calc_Nx_values(self):
        # Nx01 = None
        Nx12 = nd.cdf(self.z_list[2] - self.period_vol)\
                      - nd.cdf(self.z_list[1] - self.period_vol)
        Nx23 = nd.cdf(self.z_list[3] - self.period_vol)\
                      - nd.cdf(self.z_list[2] - self.period_vol)
        # Nx34 = nd.cdf(self.z_list[4] - self.period_vol)\
        #               - nd.cdf(self.z_list[3] - self.period_vol)
        self.Nx_list = [Nx12, Nx23]

    def calc_expected_result(self):
        # Call ExpectedResult class
        er_obj = ExpectedResult(self.S, self.high_price, self.low_price,\
                                self.bep, self.high_K, self.low_K, self.strategy,\
                                self.period_vol, self.PR_list, self.Nx_list)
        ER_list = er_obj.run_expected_result_calc()
        # Expected Result
        self.ER = round(sum(ER_list),3)
        # Collects Expected Results and Probabilities Values
        self.ER_PR_arr = np.array([ER_list, self.PR_list])

    def calc_gain_loss_probability(self):
        # ER and not self.ER in the list comprehension!!!
        PR_pos_list =\
        [self.ER_PR_arr[1][i] for i, ER in enumerate(self.ER_PR_arr[0]) if ER > 0]
        # Probability of Gain / Loss
        self.PR_gain = round(sum(PR_pos_list),3)
        self.PR_loss = round(1 - self.PR_gain,3)

    def calc_max_gain_loss(self):
        # Call GainLoss class
        gain_loss_obj = GainLoss(self.high_price, self.low_price, self.bep,\
                                 self.high_K, self.low_K, self.strategy)
        self.maxGain, self.maxLoss = gain_loss_obj.run_gain_loss_calc()

    def run_probability(self):
        self.calc_period_volatility()
        self.calc_z_values()
        self.calc_sections_probability()
        self.calc_Nx_values()
        self.calc_expected_result()
        self.calc_gain_loss_probability()
        self.calc_max_gain_loss()
        return [self.low_K, self.low_price, self.high_K, self.high_price, self.bep,\
                self.PR_gain, self.PR_loss, self.maxGain, self.maxLoss, self.ER]


class ExpectedResult:
    """
    Calculates the Expected result based on the selected spread strategy.
    """
    def __init__(self, S, high_opt_price, low_opt_price, bep, high_K, low_K, strategy,\
                period_vol, PR_list, Nx_list):
        self.S = S
        self.low_K = low_K
        self.high_K = high_K
        self.bep = bep
        self.high_price = high_opt_price
        self.low_price = low_opt_price
        self.strategy = strategy
        self.period_vol = period_vol
        self.PR_list = PR_list
        self.Nx_list = Nx_list

    def run_expected_result_calc(self):
        strategies = \
        {
            "bull_call_spread"  : \
            lambda : ExpectedResult.bull_call_ER(self.S, self.high_K, self.bep,\
            self.high_price, self.low_price, self.period_vol, self.PR_list, self.Nx_list),
            "bull_put_spread"   : \
            lambda : ExpectedResult.bull_put_ER(self.S, self.low_K, self.bep,\
            self.high_price, self.low_price, self.period_vol, self.PR_list, self.Nx_list),
        }
        return strategies[self.strategy]()

    @staticmethod
    def bull_call_ER(S, Ksc, bep, sc, lc, period_vol, PR_list, Nx_list):
        # Expected Value
        ER1 = (sc - lc) * PR_list[0]
        ER2 = S * np.exp(period_vol**2 / 2) * Nx_list[0] - bep * PR_list[1]
        ER3 = S * np.exp(period_vol**2 / 2) * Nx_list[1] - bep * PR_list[2]
        ER4 = (Ksc - bep) * PR_list[3]
        ER_list = [ER1, ER2, ER3, ER4]
        return ER_list

    @staticmethod
    def bull_put_ER(S, Klp, bep, sp, lp, period_vol, PR_list, Nx_list):
        # Expected Value
        ER1 = (Klp - bep) * PR_list[0]
        ER2 = S * np.exp(period_vol**2 / 2) * Nx_list[0] - bep * PR_list[1]
        ER3 = S * np.exp(period_vol**2 / 2) * Nx_list[1] - bep * PR_list[2]
        ER4 = (sp - lp) * PR_list[3]
        ER_list = [ER1, ER2, ER3, ER4]
        return ER_list


class GainLoss():
    """
    Calculates the Maximum Gain & Loss based on the selected spread strategy.
    """
    def __init__(self, high_opt_price, low_opt_price, bep, high_K, low_K, strategy):
        self.low_K = low_K
        self.high_K = high_K
        self.bep = bep
        self.high_price = high_opt_price
        self.low_price = low_opt_price
        self.strategy = strategy

    def run_gain_loss_calc(self):
        strategies = \
        {
            "bull_call_spread"  : \
            lambda : GainLoss.bull_call_gain_loss(self.high_K, self.bep,\
                                                  self.high_price, self.low_price),
            "bull_put_spread"   : \
            lambda : GainLoss.bull_put_gain_loss(self.low_K, self.bep,\
                                                 self.high_price, self.low_price),
        }
        return strategies[self.strategy]()

    @staticmethod
    def bull_call_gain_loss(Ksc, bep, sc, lc):
        maxGain = round(Ksc - bep,2)
        maxLoss = round(sc - lc,2)
        return maxGain, maxLoss

    @staticmethod
    def bull_put_gain_loss(Klp, bep, sp, lp):
        maxGain = round(sp - lp,2)
        maxLoss = round(Klp - bep,2)
        return maxGain, maxLoss

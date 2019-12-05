#!/usr/bin/python3


"""
---------------------------------------------------------------------------------
                            OPTIONS CALCULATOR
---------------------------------------------------------------------------------

The Black-Scholes model for European-style Options on non-dividend paying stocks.

|
| Input parameter(s):   S, K, DTE, IV, r
|                       eg. 65.0, 60.0, 30.0, 35.0, 1.6995
|

Options Pricing Parameters
--------------------------
S: Stock Price
K: Strike Price
DTE: Days to Expiration
IV: Implied Volatility (%)
r: Risk-free Rate (%)

Remark: Input parameters must be separated by comma(s).

---------------------------------------------------------------------------------
"""


__author__  = 'Zsolt Forray'
__license__ = 'MIT'
__version__ = '0.0.1'
__date__    = '26/11/2019'
__status__  = 'Development'


import math as m
from scipy.stats import norm as nd


class InvalidDataError(Exception):
    pass


class OptionPrice(object):
    def __init__(self, stock_price, strike_price, time_to_exp_days, \
                annual_vol_pc, risk_free_rate_pc):

        self.S = stock_price
        self.K = strike_price
        self.t = time_to_exp_days
        self.v = annual_vol_pc
        self.r = risk_free_rate_pc

        self.t_yrs = time_to_exp_days / 365
        self.v_dec = annual_vol_pc / 100
        self.r_dec = risk_free_rate_pc / 100

        self.check_parameters()

    def check_parameters(self):
        # check input
        CONDITIONS = [
                        self.S <= 0.0,
                        self.K <= 0.0,
                        self.t <= 0.0,
                        self.v <= 0.0,
                        self.r < 0.0
                    ]
        if any(CONDITIONS):
            raise InvalidDataError("[Error] Input parameter(s) out of range")

    def calc_d1(self):
        return (m.log(self.S / self.K) + (self.r_dec + self.v_dec**2 / 2) * self.t_yrs) \
                /(self.v_dec * m.sqrt(self.t_yrs))

    def calc_d2(self):
        d1 = self.calc_d1()
        return d1 - self.v_dec * m.sqrt(self.t_yrs)

    def call_price(self):
        d1 = self.calc_d1()
        d2 = self.calc_d2()
        callprice = self.S * nd.cdf(d1) \
                    -self.K * m.exp(-self.r_dec * self.t_yrs) * nd.cdf(d2)
        return OptionPrice.round_price(callprice)

    def put_price(self):
        d1 = self.calc_d1()
        d2 = self.calc_d2()
        putprice = self.K * m.exp(-self.r_dec * self.t_yrs) * nd.cdf(-d2) \
                   -self.S * nd.cdf(-d1)
        return OptionPrice.round_price(putprice)

    @staticmethod
    def round_price(value):
        return round(value,2)


class OptionGreeks(OptionPrice):
    """The sensitivities of the Black-Scholes Model"""

    def __init__(self, stock_price, strike_price, time_to_exp_days, \
                annual_vol_pc, risk_free_rate_pc):
        OptionPrice.__init__(self, stock_price, strike_price, time_to_exp_days, \
                             annual_vol_pc, risk_free_rate_pc)

    @staticmethod
    def round_greeks(value):
        return round(value,4)

    def call_delta(self):
        d1 = self.calc_d1()
        calldelta = nd.cdf(d1)
        return OptionGreeks.round_greeks(calldelta)

    def put_delta(self):
        putdelta = self.call_delta()-1
        return OptionGreeks.round_greeks(putdelta)

    def call_gamma(self):
        d1 = self.calc_d1()
        callgamma = nd.pdf(d1) / (self.S * self.v_dec * m.sqrt(self.t_yrs))
        return OptionGreeks.round_greeks(callgamma)

    def put_gamma(self):
        return self.call_gamma()

    def call_theta(self):
        d1 = self.calc_d1()
        d2 = self.calc_d2()
        calltheta = (-self.S * self.v_dec * nd.pdf(d1) / (2 * m.sqrt(self.t_yrs))\
                     -self.r_dec * self.K * m.exp(-self.r_dec * self.t_yrs) * nd.cdf(d2))
        calltheta = calltheta / 365
        return OptionGreeks.round_greeks(calltheta)

    def put_theta(self):
        d1 = self.calc_d1()
        d2 = self.calc_d2()
        puttheta = (-self.S * self.v_dec * nd.pdf(d1) / (2 * m.sqrt(self.t_yrs))\
                    +self.r_dec * self.K * m.exp(-self.r_dec * self.t_yrs) * nd.cdf(-d2))
        puttheta = puttheta / 365
        return OptionGreeks.round_greeks(puttheta)

    def call_vega(self):
        d1 = self.calc_d1()
        callvega = (self.S * m.sqrt(self.t_yrs) * nd.pdf(d1)) / 100
        return OptionGreeks.round_greeks(callvega)

    def put_vega(self):
        return self.call_vega()

    def call_rho(self):
        d2 = self.calc_d2()
        callrho = self.K * self.t_yrs * m.exp(-self.r_dec * self.t_yrs)\
                  * nd.cdf(d2) / 100
        return OptionGreeks.round_greeks(callrho)

    def put_rho(self):
        d2 = self.calc_d2()
        putrho = -self.K * self.t_yrs * m.exp(-self.r_dec * self.t_yrs)\
                 * nd.cdf(-d2) / 100
        return OptionGreeks.round_greeks(putrho)

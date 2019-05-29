"""
---------------------------------------------------------------------------------
                            OPTIONS CALCULATOR
---------------------------------------------------------------------------------

The Black-Scholes model for European-style Options on non-dividend paying stocks.

|
| Input parameter(s):   S, K, DTE, IV, r
|                       eg. 65.0, 60.0, 30.0, 35.0, 2.493
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

import math as m
from scipy.stats import norm as nd

class InvalidDataError(Exception):
    pass

class OptionPricing(object):
    def __init__(self, stock_price, strike_price, time_to_exp_days, \
                annual_vol_pc, risk_free_rate_pc):

        self.S = stock_price
        self.K = strike_price
        self.t = time_to_exp_days
        self.v = annual_vol_pc
        self.r = risk_free_rate_pc

        # check input
        if (self.S <= 0.0 or self.K <= 0.0 or self.t <= 0.0 \
            or self.v <= 0.0 or self.r < 0.0):
            raise InvalidDataError("[Error] Input parameter(s) out of range")

        self.t_yrs = time_to_exp_days / 365
        self.v_dec = annual_vol_pc / 100
        self.r_dec = risk_free_rate_pc / 100

        self.d = (m.log(self.S / self.K) + (self.r_dec + self.v_dec ** 2 / 2) * \
                self.t_yrs) / (self.v_dec * m.sqrt(self.t_yrs))

        self.X2c = nd.cdf(self.d - self.v_dec * m.sqrt(self.t_yrs))
        self.X2p = nd.cdf(self.v_dec * m.sqrt(self.t_yrs) - self.d)

    def price(self):
        X0c = self.S * nd.cdf(self.d)
        X0p = -self.S * nd.cdf(-self.d)
        X1 = self.K * m.exp(-self.r_dec * self.t_yrs)
        call_price = round(X0c - X1 * self.X2c, 2)
        put_price = round(X0p + X1 * self.X2p, 2)
        return {"call":round(call_price,2), "put":round(put_price,2)}

    # The sensitivities of the Black-Scholes Model
    def delta(self):
        call_delta = nd.cdf(self.d)
        put_delta = -nd.cdf(-self.d)
        return {"call":round(call_delta,4), "put":round(put_delta,4)}

    def gamma(self):
        call_gamma = nd.pdf(self.d) / (self.S * self.v_dec * m.sqrt(self.t_yrs))
        put_gamma = call_gamma
        return {"call":round(call_gamma,4), "put":round(put_gamma,4)}

    def theta(self):
        X0 = -self.S * self.v_dec * nd.pdf(self.d) / (2 * m.sqrt(self.t_yrs))
        X1 = self.r_dec * self.K * m.exp(-self.r_dec * self.t_yrs)
        call_theta = (X0 - X1 * self.X2c) / 365
        put_theta = (X0 + X1 * self.X2p) / 365
        return {"call":round(call_theta,4), "put": round(put_theta,4)}

    def vega(self):
        call_vega = (self.S * m.sqrt(self.t_yrs) * nd.pdf(self.d)) / 100
        put_vega = call_vega
        return {"call":round(call_vega,4), "put": round(put_vega,4)}

    def rho(self):
        X0 = self.t_yrs * self.K * m.exp(-self.r_dec * self.t_yrs)
        call_rho = X0 * self.X2c / 100
        put_rho = -X0 * self.X2p / 100
        return {"call":round(call_rho,4), "put": round(put_rho,4)}

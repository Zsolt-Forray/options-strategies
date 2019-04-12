"""
--------------------------------------------------------------------------------
                        OPTIONS STRATEGY ANALYZING TOOL
--------------------------------------------------------------------------------

Options Strategy Analyzing Framework

The best options strategy is selected based on the largest Expected Result (ER).

|
| Input parameter(s):   S, DTE, IV, r, strategy, chart
|                       eg. 40.0, 30.0, 40.0, 2.5136, "bull_call_spread", True
|

Strategy: Options Strategies
                    "bull_call_spread"
                    "bull_put_spread"

Options Pricing Parameters
--------------------------
S: Price of the underlying asset (20-200).
DTE: Number of days to expiration (1-360).
IV: Estimated future volatility of a security's price (10-150).
r: Risk-free interest rate (1-4).
chart: If `True`, the "Payoff diagram" is shown.

Remark: Input parameters must be separated by comma(s).

--------------------------------------------------------------------------------
"""

import numpy as np
from itertools import product
import matplotlib.pyplot as plt

# import strategies
import strategy_bull_call_spread as bull_cs
import strategy_bull_put_spread as bull_ps

# TODO: other strategies can be added later

class InvalidStrategyError(Exception):
    pass
class InvalidDataError(Exception):
    pass

def create_strike_pairs(S0, strategy):
    """ Creates list of strike pairs for options strategies """

    RNG = 5     # range for the boundaries of strike prices
    STEP = 0.5  # step for strike prices
    if RNG >= S0:
        raise InvalidDataError()

    # Min/Max Strike Price
    Kmin = S0 - RNG
    Kmax = S0 + RNG
    lower_strike = np.arange(int(Kmin), int(Kmax)+0.1, STEP)
    higher_strike = np.arange(int(Kmin), int(Kmax)+0.1, STEP)
    strike_pairs_list = list(product(lower_strike, higher_strike))

    strike_list = []
    if strategy in ["short_straddle", "long_naked_call", "short_naked_put"]:
        for k in strike_pairs_list:
            if k[0] == k[1]:
                strike_list.append(k)
    # Bull Call Spread, Bull Put Spread, etc.
    else:
        for k in strike_pairs_list:
            if k[0] < k[1]:
                strike_list.append(k)

    # The first value in the strike list belongs to the lower strike
    # The second one belongs to the higher one
    return strike_list

def run_analyzing_tool(S0, DTE0, IV0, r, strategy, strike_list):
    # Stock price range from the min/max strike price for payoff calculation
    rng_stock = 15

    COLS_BULL_CALL_SPREAD = ["Kpc", "Ppc", "Ksc", "Psc", "BEP", "Prob.G",
                            "Prob.L", "Max.G", "Max.L", "ER"]
    COLS_BULL_PUT_SPREAD = ["Kpp", "Ppp", "Ksp", "Psp", "BEP", "Prob.G",
                            "Prob.L", "Max.G", "Max.L", "ER"]

    # K_dict: [module name, columns, Klower, Khigher, price1, price2]
    K_dict = {
                "bull_call_spread": [bull_cs, COLS_BULL_CALL_SPREAD, 0, 2, 1, 3],
                "bull_put_spread": [bull_ps,COLS_BULL_PUT_SPREAD,0,2,1,3],
            }

    res_list = []
    selected = False
    for vals in strike_list:
        Klower = vals[0]
        Khigher = vals[1]

        strat_module = K_dict[strategy][0].run_strategy

        res_row = strat_module(S0, Klower, Khigher, DTE0, IV0, r, selected, strike_list, rng_stock)

        #---------------------------------------------------------
        # Price of the 2 legs of options must be greater than 0.08
        # The Expected Result (ER) must be greater than 0.05
        if res_row[K_dict[strategy][4]] > 0.08 \
           and res_row[K_dict[strategy][5]] > 0.08 \
           and res_row[-1] > 0.05:
            res_list.append(res_row)
        #---------------------------------------------------------

    res_list = sorted(res_list, key=lambda l:l[9], reverse=True)

    chart_data = None
    if len(res_list) > 0:

        selected = True

        selected_Klower = res_list[0][K_dict[strategy][2]]
        selected_Khigher = res_list[0][K_dict[strategy][3]]

        # Calculates the Profit/Loss curve for the selected trade
        chart_data = strat_module(S0, selected_Klower, selected_Khigher,
                                    DTE0, IV0, r, selected, strike_list, rng_stock)

    else:
        msg = "[Info] No Strategy Found with Positive Expected Return (ER)"
        print(msg)

    return res_list, chart_data

def display_result(chart_data, strategy):
    # Drawing Chart
    plt.plot(chart_data[0], chart_data[1])
    plt.title("Profit / Loss Profile\nStrategy: {}".format(strategy))
    plt.ylabel("Profit / Loss")
    plt.xlabel("Stock Price")
    plt.grid(True)
    plt.show()

def run(S, DTE, IV, r, strategy, chart=False):
    strategies = ["bull_call_spread", "bull_put_spread"]

    try:
        if strategy not in strategies:
            raise InvalidStrategyError()

        if (S < 20.0 or S > 200.0)\
            or (DTE < 1.0 or DTE > 360.0)\
            or (IV < 10.0 or IV > 150.0)\
            or (r < 1.0 or r > 4.0):
            raise InvalidDataError()

        strike_pairs = create_strike_pairs(S, strategy)
        res, chart_data = run_analyzing_tool(S, DTE, IV,
                            r, strategy, strike_pairs)

        if chart_data != None and chart == True:
            display_result(chart_data, strategy)

        return res

    except InvalidStrategyError:
        print("[Error] Invalid strategy is selected")
    except InvalidDataError:
        print("[Error] Please check the input parameters")


if __name__ == "__main__":
    run(40,40,45,2,"bull_call_spread", True)

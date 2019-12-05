#!/usr/bin/python3


"""
--------------------------------------------------------------------------------
                        OPTIONS STRATEGY ANALYZING TOOL
--------------------------------------------------------------------------------

Options Strategy Analyzing Framework

The best options strategy is selected based on the largest Expected Result (ER).

| Input parameter(s):   S, DTE, IV, rate, strategy, show_chart
|                       eg. 40.0, 30.0, 40.0, 2.5136, "bull_put_spread", True

Strategy: Currently Available Spread Options Strategies
                                "bull_call_spread"
                                "bull_put_spread"

Options Pricing Parameters (suggested)
------------------------------------------
S:          Price of the underlying asset (10-200).
DTE:        Number of days to expiration (1-360).
IV:         Estimated future volatility of a security's price (10-150).
rate:       Risk-free interest rate (1-4).
show_chart: If `True`, the "Payoff diagram" is shown.

| Output: Lists of trade opportunities having parameters as:
          0: Lower Strike
          1: Options Value for the Lower Strike
          2: Higher Strike
          3: Options Value for the Higher Strike
          4: Break Even Point
          5: Probability of Gain
          6: Probability of Loss
          7: Maximum Gain
          8: Maximum Loss
          9: Expected Result

Remark: Input parameters must be separated by comma(s).

--------------------------------------------------------------------------------
"""


__author__  = 'Zsolt Forray'
__license__ = 'MIT'
__version__ = '0.0.1'
__date__    = '05/12/2019'
__status__  = 'Development'


import numpy as np
from itertools import product
import matplotlib.pyplot as plt
from strategy_spread import Spread
from user_defined_exceptions import NoTradeFoundError
from user_defined_exceptions import InvalidStrategyError
from user_defined_exceptions import InvalidDataError


class Framework:
    """
    Main class for options strategy calculation.
    """
    def __init__(self, S, DTE, IV, rate, strategy, show_chart):
        self.S = S
        self.DTE = DTE
        self.IV = IV
        self.rate = rate
        self.strategy = strategy
        self.show_chart = show_chart

    def create_strike_pairs(self):
        """Creates list of strike pairs for options strategies"""
        RNG_STRIKE = 5              # Strike price range from the stock price
        STRIKE_PRICE_STEP = 0.5     # step for strike prices
        if RNG_STRIKE+1 >= self.S:  # one added to avoid strike equal to zero
            raise InvalidDataError()

        # Min/Max Strike Price
        Kmin = self.S - RNG_STRIKE
        Kmax = self.S + RNG_STRIKE
        lower_strike = np.arange(int(Kmin), int(Kmax)+0.1, STRIKE_PRICE_STEP)
        higher_strike = np.arange(int(Kmin), int(Kmax)+0.1, STRIKE_PRICE_STEP)
        strike_pairs_list = list(product(lower_strike, higher_strike))

        strike_list = []
        if self.strategy in ("short_straddle", "long_naked_call", "short_naked_put"):
            for k in strike_pairs_list:
                if k[0] == k[1]:
                    strike_list.append(k)

        elif self.strategy in ("bull_call_spread", "bull_put_spread"):
            for k in strike_pairs_list:
                if k[0] < k[1]:
                    strike_list.append(k)
        # The first value in the strike list represents the lower strike.
        # The second one represents the higher one.
        return strike_list

    def get_all_results(self, strike_pairs):
        """Results are sorted from the highest ER to the lowest"""
        res_list = []
        for vals in strike_pairs:
            Klower = vals[0]
            Khigher = vals[1]
            spread_obj = Spread(self.S, Klower, Khigher, self.DTE, self.IV,\
                                self.rate, self.strategy)
            res_row = spread_obj.run_strategy()

            low_price = res_row[1]
            high_price = res_row[3]
            ER = res_row[-1]
            # Price of the 2 legs of options must be greater than 0.08.
            # The Expected Result (ER) must be greater than 0.08.
            if all(i > 0.08 for i in [low_price, high_price, ER]):
                res_list.append(res_row)
        res_list.sort(key=lambda x:x[9], reverse=True)

        if len(res_list) == 0:
            raise NoTradeFoundError()
        return res_list

    def get_selected_best_result(self, res_list):
        """Select the best (the highest ER) trade for Payoff diagram"""
        chart_data = None
        if self.show_chart:
            selected_Klower = res_list[0][0]
            selected_Khigher = res_list[0][2]
            # Calculates the Profit/Loss curve for the selected trade
            spread_obj = Spread(self.S, selected_Klower, selected_Khigher,\
                                self.DTE, self.IV, self.rate, self.strategy)
            stock_price_arr, payoff_arr = spread_obj.collect_chart_data()
            chart_data = [stock_price_arr, payoff_arr]
        return chart_data

    def display_result(self, chart_data):
        strategy_name = self.strategy.replace("_", " ").title()
        # Drawing Chart
        plt.plot(chart_data[0], chart_data[1])
        plt.title("Profit / Loss Profile\nStrategy: {}".format(strategy_name))
        plt.ylabel("Profit / Loss")
        plt.xlabel("Stock Price")
        plt.grid(True)
        plt.show()

    def run_app(self):
        strategies = ["bull_call_spread", "bull_put_spread"]
        try:
            if self.strategy not in strategies:
                raise InvalidStrategyError()

            strike_pairs = self.create_strike_pairs()
            res_list = self.get_all_results(strike_pairs)
            chart_data = self.get_selected_best_result(res_list)

            if chart_data is not None and self.show_chart:
                self.display_result(chart_data)
            return res_list

        except NoTradeFoundError:
            print("[Error] No valid trade found")
        except InvalidStrategyError:
            print("[Error] Invalid strategy is selected")
        except InvalidDataError:
            print("[Error] Please check the input parameters")


if __name__ == "__main__":
    fw_obj = Framework(50,80,10,2.5136,"bull_put_spread",True)
    fw_obj.run_app()

# options-strategies

## Description
This project includes options calculator and options strategy analyzing tool:

- [Options Calculator](#options-calculator)
- [Options Strategy Analyzing Tool](#options-strategy-analyzing-tool)

## Usage
1.  Create a new directory somewhere.
2.  Open the Start Menu, type `cmd` in the search field, and then press Enter.
3.  Clone the project by running (make sure that you are in the newly created directory first!):
```
git clone https://github.com/Zsolt-Forray/options-strategies.git
```
4.  Tools are found in the `options-strategies` folder.

## Options Calculator
Calculates the value of Call/Put European options on non-dividend paying stocks and the Greeks.

### Usage Example

#### Parameters:
+   S: Stock Price (20-200)
+   K: Strike Price (20-200)
+   DTE: Days to Expiration (1-360)
+   IV: Implied Volatility (%) (10-150)
+   r: Risk-free Rate (%) (1-4)

```
import option_pricing_black_scholes as op
import pprint

pp = pprint.PrettyPrinter(indent=4)

res = op.run(S=65, K=60, DTE=30, IV=35, r=2.493)

pp.pprint(res)
```

### Output
Dictionary: theoretical prices and the Greeks for European style call and put options.

![Screenshot](/png/opt_calc_output.png)

## Options Strategy Analyzing Tool
Calculates the Expected Result (ER) of options strategies based on different strike prices. Trades with positive expected results are selected and these trade opportunities are sorted from the highest ER to the lowest.

### Usage Example

#### Parameters:
+   S: Stock Price (20-200)
+   DTE: Days to Expiration (1-360)
+   IV: Implied Volatility (%) (10-150)
+   r: Risk-free Rate (%) (1-4)
+   strategy: There are 2 strategies available. Select one of them: `"bull_put_spread", "bull_call_spread"`.
+   chart: If `True`, the "Payoff diagram" is shown. The default is `False`.

```
import options_strategy_analyzing_framework as osf

# Strategies should be in the same folder

res = osf.run(S=40, DTE=30, IV=40, r=2.5136, strategy="bull_put_spread", chart=True)

pp.pprint(res)
```

### Output
2-D list: Options trades with positive expected result are calculated and their parameters are collected in lists. The highest ER trade can be obtained as: `res[0]`.

![Screenshot](/png/opt_strategy_output.png)

Accessible parameters of the highest ER trade (list index: value) are:
+   0: Lower strike price
+   1: Option value belongs to the lower strike price
+   2: Higher strike price
+   3: Option value belongs to the higher strike price
+   4: Break Even Point (BEP)
+   5: Probability of Gain
+   6: Probability of Loss
+   7: Maximum Gain
+   8: Maximum Loss
+   9: Expected Result (ER)

#### Payoff Diagram

![Screenshot](/png/payoff_chart.png)

## LICENSE
MIT

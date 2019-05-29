# options-strategies

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/97645bd4d71b41e5a175cd2d10465a11)](https://www.codacy.com/app/forray.zsolt/options-strategies?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Zsolt-Forray/options-strategies&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/97645bd4d71b41e5a175cd2d10465a11)](https://www.codacy.com/app/forray.zsolt/options-strategies?utm_source=github.com&utm_medium=referral&utm_content=Zsolt-Forray/options-strategies&utm_campaign=Badge_Coverage)
[![Build Status](https://travis-ci.com/Zsolt-Forray/options-strategies.svg?branch=master)](https://travis-ci.com/Zsolt-Forray/options-strategies)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Description
This project includes options strategy analyzing tool:

## Usage
1.  Create a new directory somewhere.
2.  Open the Start Menu, type `cmd` in the search field, and then press Enter.
3.  Clone the project by running (make sure that you are in the newly created directory first!):
```txt
git clone https://github.com/Zsolt-Forray/options-strategies.git
```
4.  Tool is found in the `options-strategies` folder.

## Options Strategy Analyzing Tool
Calculates the Expected Result (ER) of options strategies based on different strike prices. Trades with positive expected results are selected and these trade opportunities are sorted from the highest ER to the lowest.

### Usage Example

#### Parameters (suggested):
+   S: Stock Price (20-200)
+   DTE: Days to Expiration (1-360)
+   IV: Implied Volatility (%) (10-150)
+   r: Risk-free Rate (%) (1-4)
+   strategy: There are 2 strategies available. Select one of them: `"bull_put_spread", "bull_call_spread"`.
+   chart: If `True`, the "Payoff diagram" is shown. The default is `False`.

```python
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

## Contributions
Contributions to Options Strategies are always welcome.  
If you have questions, suggestions or want to improve this repository, please create an [issue](https://github.com/Zsolt-Forray/options-strategies/issues) or [pull requests](https://github.com/Zsolt-Forray/options-strategies/pulls).  
This repo is maintained by Zsolt Forray (forray.zsolt@gmail.com).

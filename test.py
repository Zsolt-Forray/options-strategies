import unittest
import options_strategy_analyzing_framework as osf
from options_strategy_analyzing_framework import InvalidDataError


class TestFramework(unittest.TestCase):
    def test_bull_call__spread_res(self):
        data = (60, 30, 40, 2.5136, "bull_call_spread", True)
        result = [55.0, 5.94, 65.0, 1.06, 59.88, 0.507, 0.493, 5.12, -4.88, 0.154]
        self.assertEqual(osf.run(*data)[0], result)

    def test_bull_put__spread_res(self):
        data = (60, 30, 40, 2.5136, "bull_put_spread", True)
        result = [55.0, 0.82, 65.0, 5.92, 59.9, 0.506, 0.494, 5.1, -4.9, 0.134]
        self.assertEqual(osf.run(*data)[0], result)

    def test_invalid_stock_price(self):
        data = (1, "bull_put_spread")
        with self.assertRaises(InvalidDataError):
            osf.create_strike_pairs(*data)

    def test_invalid_strategy(self):
        data = (60, 30, 40, 2.5136, "short_straddle", True)
        self.assertEqual(osf.run(*data), None)

    def test_no_res_strategy(self):
        data = (50, 30, 4, 2.5136, "bull_put_spread", False)
        self.assertEqual(osf.run(*data), [])


if __name__ == "__main__":
    unittest.main()

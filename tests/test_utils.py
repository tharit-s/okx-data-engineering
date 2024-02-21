import unittest
import pandas as pd
from src.utils import (
    create_dataframe_from_dict
)
import configparser

config = configparser.ConfigParser()
config.read('config/base.ini')

limit = int(config['okx.MarketData.get_history_trades']['limit'])

class TestUtils(unittest.TestCase):
    def test_create_dataframe_from_dict(self):
        # input
        data = {
            "col1": [1, 2, 3],
            "col2": [4, 5, 6]
        }
        dict = [
            {"col1": 1, "col2": 4},
            {"col1": 2, "col2": 5},
            {"col1": 3, "col2": 6},
        ]
        # expected result
        expected_df = pd.DataFrame(data)
        # actual result
        actual_df = create_dataframe_from_dict(dict)
        pd.testing.assert_frame_equal(expected_df, actual_df)

if __name__ == '__main__':
   unittest.main()
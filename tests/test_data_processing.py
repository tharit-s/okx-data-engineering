import unittest
import pandas as pd
from src.data_processing import get_history_trades
import configparser

config = configparser.ConfigParser()
config.read('config/base.ini')

limit = int(config['okx.MarketData.get_history_trades']['limit'])

class TestDataProcessing(unittest.TestCase):
    def test_count_members(self):
        # input
        instrument_id = "XRP-USDT"
        start_id = ""
        end_id = ""
        # expected result
        expected_count_members = limit
        # actual result
        output_data = get_history_trades(instrument_id=instrument_id, start_id=start_id, end_id=end_id)
        actual_count_members = len(output_data["data"])
        self.assertEqual(expected_count_members, actual_count_members)

    def test_exclusive_range(self):
        # input
        instrument_id = "XRP-USDT"
        start_id = "131003137" # exclusive start id
        end_id = "131003146" # exclusive end id
        # expected result
        expected_count_members_removed_exclusive_start_and_end = limit - 2
        # actual result
        output_data = get_history_trades(instrument_id=instrument_id, start_id=start_id, end_id=end_id)
        actual_count_members = len(output_data["data"])
        self.assertEqual(expected_count_members_removed_exclusive_start_and_end, actual_count_members)

if __name__ == '__main__':
   unittest.main()
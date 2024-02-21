from src.data_processing import (
    get_history_trades
)
from src.utils import (
    create_dataframe_from_dict,
    write_df_to_csv_on_local,
    get_latest_id_from_df,
    write_checkpoint,
    read_checkpoint
)
from constants import (
    FULL_LOAD,
    INCREMENTAL_LOAD,
    LOCAL,
    GOOGLE_SHEETS
)
import configparser
import pandas as pd


config = configparser.ConfigParser()
config.read('config/base.ini')

checkpoint_data = {}

class DataIngestion():

    def __init__(self, ingestion_method="FULL_LOAD", instrument_id="XRP-USDT", start_id="", end_id=""):
        self.ingestion_method = ingestion_method
        self.instrument_id = instrument_id
        self._set_id_range(start_id, end_id)
        self._validate_ids()
        self.limit = int(config['okx.MarketData.get_history_trades']['limit'])

    def _set_id_range(self, start_id, end_id):
        print(self.ingestion_method)
        if self.ingestion_method == FULL_LOAD:
            self.start_id = start_id if len(start_id) > 0 else self._get_default_start_id()
            self.end_id = end_id if len(start_id) > 0 else self._get_default_end_id()
        elif self.ingestion_method == INCREMENTAL_LOAD:
            checkpoint_data = read_checkpoint()
            latest_id = checkpoint_data["latest_id"]
            self.start_id = str(latest_id)
            self.end_id = ""
        else:
            raise ValueError("Invalid ingestion method")
    
    def _validate_ids(self):
        if self.start_id == '' and self.end_id == '':
            raise ValueError("Both start_id and end_id must be non-empty values.")
    
    def _get_default_start_id(self):
        default_start_id = "131003137"
        return default_start_id

    def _get_default_end_id(self):
        default_end_id = "131003146"
        return default_end_id

    def extract_data(self, start_id, end_id):
        response = get_history_trades(
            instrument_id=self.instrument_id, 
            start_id=start_id, 
            end_id=end_id
        )
        return response

    def incremental_load(self):
        incremental_data = []
        print(f"Exclusive start id: {self.start_id}")
        print(f"Exclusive end id: {self.end_id}")

        while True:
            print(f"Start id: {self.start_id}")
            print(f"End id: {self.end_id}")
            data = self.extract_data(self.start_id, self.end_id)
            data = data["data"]
            print(f"Number of records: {len(data)}")
            incremental_data.extend(data)
            print(f"Number of records appended: {len(incremental_data)}")
            print("---")
            if len(data) == self.limit:
                if self.end_id == "":
                    latest_start_id = data[0]["tradeId"]
                    self.start_id = latest_start_id
                else:
                    latest_end_id = data[-1]["tradeId"]
                    self.end_id = latest_end_id
            else:
                break
        return incremental_data

    def transform_data(self, raw_data):
        transformed_data = create_dataframe_from_dict(raw_data)
        return transformed_data

    def load_data(self, transformed_data, load_method):
        if load_method == LOCAL:
            print("Loading to Local")
            self.load_to_local(transformed_data)
        elif load_method == GOOGLE_SHEETS:
            print("Loading to Google Sheets")
            self.load_to_google_sheets()
        else:
            print("Invalid load method")
    
    def load_to_local(self, transformed_data):
        now_utc = pd.to_datetime('now', utc=True)
        file_extension = config['src.data_ingestion.trade.load_data']['file_extension']
        output_folder = config['src.data_ingestion.trade.load_data']['output_folder']
        filename = f"{self.instrument_id}_{now_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}.csv"
        data_dir = f"{output_folder}/{now_utc.strftime('%Y-%m-%d')}"
        write_df_to_csv_on_local(transformed_data, filename, data_dir)
            
    def load_to_google_sheets(self, transformed_data):
        write_data_to_google_sheets(transformed_data)

    def run_pipeline(self):
        print(f"Instrument id: {self.instrument_id}")
        raw_data = self.incremental_load()
        transformed_data = self.transform_data(raw_data)
        if transformed_data.empty:
            print(f"No data between start_id: {self.start_id} and end_id: {self.end_id}")
        else:
            latest_id = get_latest_id_from_df(transformed_data, column_name="tradeId")
            print(transformed_data.head())
            self.load_data(transformed_data, load_method=LOCAL)
            # self.load_data(transformed_data, load_method=GOOGLE_SHEETS)
            write_checkpoint(checkpoint_data, latest_id)
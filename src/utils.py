import pandas as pd
import os
import json
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config/base.ini')


def create_dataframe_from_dict(raw_data_dict):
    df = pd.DataFrame.from_dict(raw_data_dict, orient='columns')
    return df

def write_df_to_csv_on_local(df, filename, data_dir):
    # Create directories if needed
    os.makedirs(data_dir, exist_ok=True)

    # Construct full filepath
    filepath = os.path.join(data_dir, filename)

    # Write DataFrame to CSV
    df.to_csv(filepath, index=False)

    print(f"CSV file saved to: {filepath}")

def get_latest_id_from_df(df, column_name):
    sorted_df = df.sort_values(column_name, ascending=False)
    latest_data = sorted_df.iloc[0]
    latest_id = latest_data[column_name]
    return latest_id


def write_checkpoint(data, latest_id):
    # Get current UTC timestamp
    utc_timestamp = datetime.now().isoformat()

    # Create or update data dictionary
    if data:
        data["utc_timestamp"] = utc_timestamp
        data["latest_id"] = latest_id
    else:
        data = {"utc_timestamp": utc_timestamp, "latest_id": latest_id}

    # Write data to JSON file
    with open("config/checkpoint.json", "w") as f:
        json.dump(data, f, indent=4)

def read_checkpoint():
  try:
    with open("config/checkpoint.json", "r") as f:
      data = json.load(f)
      return data
  except (FileNotFoundError, json.JSONDecodeError):
    return None
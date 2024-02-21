from src.data_ingestion.trade import DataIngestion
import configparser

config = configparser.ConfigParser()
config.read('config/base.ini')

ingestion_method = config['src.data_ingestion.trade']['ingestion_method']
instrument_id = config['src.data_ingestion.trade']['instrument_id']
start_id = config['src.data_ingestion.trade']['start_id']
end_id = config['src.data_ingestion.trade']['end_id']

if __name__ == "__main__":
    data_ingestion = DataIngestion(
        ingestion_method=ingestion_method,
        instrument_id=instrument_id,
        start_id=start_id,
        end_id=end_id
    )
    data_ingestion.run_pipeline()
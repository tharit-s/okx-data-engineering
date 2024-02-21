import okx.MarketData as MarketData
import configparser

config = configparser.ConfigParser()
config.read('config/base.ini')

flag = config['DEFAULT']['flag']

def get_history_trades(instrument_id="XRP-USDT", start_id="131003137", end_id="131003146"):
    marketDataAPI =  MarketData.MarketAPI(flag=flag)
    type = config['okx.MarketData.get_history_trades']['type']
    limit = config['okx.MarketData.get_history_trades']['limit']

    # Retrieve the recent transactions of an instrument from the last 3 months with pagination
    response = marketDataAPI.get_history_trades(
        instId=instrument_id,
        type=type,
        after=end_id, # end id
        before=start_id, # start id
        limit=limit
    )
    return response
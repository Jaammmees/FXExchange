from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import config
import pandas as pd
import pytz
from datetime import datetime

api = API(access_token=config.access_token)

def fetch_fx_data(instrument, granularity, count=50):
    params = {"count": count, "granularity": granularity}
    candles = instruments.InstrumentsCandles(instrument=instrument, params=params)
    response = api.request(candles)
    
    # Prepare data for candlestick chart
    data = []
    for candle in response['candles']:
        time = pd.to_datetime(candle['time'])
        open_price = float(candle['mid']['o'])
        high_price = float(candle['mid']['h'])
        low_price = float(candle['mid']['l'])
        close_price = float(candle['mid']['c'])
        volume = float(candle['volume'])
        data.append([time, open_price, high_price, low_price, close_price, volume])
    
    df = pd.DataFrame(data, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df.set_index('Time', inplace=True)
    adelaide_tz = pytz.timezone('Australia/Adelaide')
    df.index = df.index.tz_convert(adelaide_tz)
    
    return df
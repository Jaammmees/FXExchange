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

def fetch_order_book(instrument):
    api = API(access_token=config.access_token)
    order_book_endpoint = instruments.InstrumentsOrderBook(instrument=instrument)
    response = api.request(order_book_endpoint)
    #print(response) 

    # Extract the buckets from the response
    buckets = response['orderBook']['buckets']
    
    # Prepare data for DataFrame
    prices = []
    long_counts = []
    short_counts = []
    for bucket in buckets:
        prices.append(float(bucket['price']))
        long_counts.append(float(bucket['longCountPercent']))  # Convert percentage to float
        short_counts.append(float(bucket['shortCountPercent']))  # Convert percentage to float
    
    # Create a DataFrame
    data = {
        'Price': prices,
        'Long Count Percent': long_counts,
        'Short Count Percent': short_counts
    }
    
    order_book_df = pd.DataFrame(data)
    
    return order_book_df


def process_fx_data(data):
    prices = [float(candle['mid']['c']) for candle in data['candles']]
    timestamps = [candle['time'] for candle in data['candles']]
    return timestamps, prices

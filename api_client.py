from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import config

api = API(access_token=config.access_token)

def fetch_fx_data(instrument, count=50, granularity='M5'):
    params = {"count": count, "granularity": granularity}
    candles = instruments.InstrumentsCandles(instrument=instrument, params=params)
    api.request(candles)
    return candles.response

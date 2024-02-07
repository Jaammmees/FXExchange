from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import config

api = API(access_token=config.access_token)

def execute_trade(instrument, units):
    data = {
        "order": {
            "instrument": instrument,
            "units": units,
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }
    order = orders.OrderCreate(accountID=config.account_id, data=data)
    response = api.request(order)
    print(response)

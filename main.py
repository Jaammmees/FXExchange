import api_client
import data_processing
import plotting
import trading

def main():
    instrument = "AUD_USD"
    data = api_client.fetch_fx_data(instrument)
    timestamps, prices = data_processing.process_fx_data(data)
    plotting.plot_fx_data(timestamps, prices, instrument)
    
    # Example trading action
    # Uncomment the next line to enable trading functionality
    # trading.execute_trade(instrument, 100)  # Buy 100 units of EUR_USD

if __name__ == "__main__":
    main()

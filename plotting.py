import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_fx_data(timestamps, prices, instrument):
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, prices, label=instrument)
    plt.title(f"FX Price for {instrument}")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%dT%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.legend()
    plt.show()

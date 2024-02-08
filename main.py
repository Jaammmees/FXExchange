import mplfinance as mpf
import matplotlib.animation as animation
import api_client

instrument = "AUD_USD"
df = api_client.fetch_fx_data(instrument)  # Initial data fetch

fig, axes = mpf.plot(df, type='candle', style='yahoo', returnfig=True)

def animate(ival):
    global df
    df = api_client.fetch_fx_data(instrument)  # Fetch updated data
    axes[0].clear()
    mpf.plot(df, ax=axes[0], type='candle', style='yahoo')

ani = animation.FuncAnimation(fig, animate, interval=100, cache_frame_data=False)

mpf.show()

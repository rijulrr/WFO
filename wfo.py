import vectorbt as vbt
import numpy as np
import pandas as pd


vbt.settings.data['alpaca']['key_id'] = 'PK4Q25GWBEYF7OVQNOUE'
vbt.settings.data['alpaca']['secret_key'] = 'm3beKLmXaMdHtt6SZqutBP33Wzk179QTHbnhkRKe'

alpacadata = vbt.AlpacaData.download('SPY', start='2017-01-01', end='2022-01-01', timeframe='1d', limit=10000)

closing_price = alpacadata.get('Close')

#figure = closing_price.vbt.plot(trace_names=['Price'], width=1280, height=720)

#figure.show()

windows = np.arange(10, 50)
fast_ma, slow_ma = vbt.MA.run_combs(closing_price, windows)
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

portfolio = vbt.Portfolio.from_signals(closing_price, entries, exits, freq='1d', direction='both')

print(portfolio.total_return().sort_values())






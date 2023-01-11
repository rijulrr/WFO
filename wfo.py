import vectorbt as vbt
import numpy as np
import pandas as pd


vbt.settings.data['alpaca']['key_id'] = 'PK4Q25GWBEYF7OVQNOUE'
vbt.settings.data['alpaca']['secret_key'] = 'm3beKLmXaMdHtt6SZqutBP33Wzk179QTHbnhkRKe'

alpacadata = vbt.AlpacaData.download('SPY', start='2017-01-01', end='2022-01-01', timeframe='1d', limit=10000)

closing_price = alpacadata.get('Close')
'''
- Plotting price data for a particular symbol

figure = closing_price.vbt.plot(trace_names=['Price'], width=1280, height=720)
figure.show()
'''

'''
- Simulating the params

windows = np.arange(10, 50)
fast_ma, slow_ma = vbt.MA.run_combs(closing_price, windows)
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

portfolio = vbt.Portfolio.from_signals(closing_price, entries, exits, freq='1d', direction='both')

print(portfolio.total_return().sort_values())
'''


'''
- Example to show how the moving average crossover strategy is ineffective

future_price = vbt.AlpacaData.download('SPY', start='2022-06-01', end='2023-01-09', timeframe='1d', limit=10000).get('Close')

fast_ma = vbt.MA.run(future_price, 30)
slow_ma = vbt.MA.run(future_price, 40)

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

portfolio = vbt.Portfolio.from_signals(future_price, entries, exits, freq='1d', direction='both')

print(portfolio.total_return())
'''

'''
- implementing the walk forward analysis

# choosing 360 since 70% of 360 is 252, the approx num of trading days
figure = closing_price.vbt.rolling_split(n=20, window_len=360, set_lens=(108,), left_to_right=False, plot=True)
figure.update_layout(height=1280, width=720)
figure.show()
'''


(in_sample_prices, in_sample_dates), (out_sample_prices, out_sample_dates) = closing_price.vbt.rolling_split(n=20, window_len=360, set_lens=(108,), left_to_right=False)

windows = np.arange(10, 50)
fast_ma, slow_ma = vbt.MA.run_combs(in_sample_prices, windows)
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

portfolio = vbt.Portfolio.from_signals(in_sample_prices, entries, exits, freq='1d', direction='both')

# gives you moving avg windows optimized on the split 
performace = portfolio.sharpe_ratio()

# returns best set of paramaters for the in_sample price sets
print(performace[performace.groupby('split_idx').idxmax()].index)

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Load the CHF/JPY data from Yahoo Finance
data = yf.download('CHFJPY=X', start='2022-01-01', end='2024-08-30')

# Function to calculate cumulative returns
def calculate_cumulative_returns(signals):
    signals['returns'] = signals['price'].pct_change()
    signals['strategy_returns'] = signals['signal'].shift(1) * signals['returns']
    signals['cumulative_returns'] = (1 + signals['strategy_returns']).cumprod()
    return signals

# Simple Moving Averages Strategy
def SMA_strategy(data, short_window=50, long_window=200):
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    signals['signal'] = 0.0
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    
    # Calculate cumulative returns
    signals = calculate_cumulative_returns(signals)
    
    # Plotting - Price and Signals
    plt.figure(figsize=(12, 8))
    plt.plot(signals['price'], label='CHF/JPY Price', color='black')
    plt.plot(signals['short_mavg'], label=f'{short_window}-day SMA', color='blue')
    plt.plot(signals['long_mavg'], label=f'{long_window}-day SMA', color='red')
    plt.plot(signals[signals['positions'] == 1.0].index, 
             signals['short_mavg'][signals['positions'] == 1.0],
             '^', markersize=10, color='g', label='Buy Signal')
    plt.plot(signals[signals['positions'] == -1.0].index, 
             signals['short_mavg'][signals['positions'] == -1.0],
             'v', markersize=10, color='r', label='Sell Signal')
    plt.title('Simple Moving Average Strategy')
    plt.legend()
    plt.show()
    
    # Plotting - Cumulative Returns
    plt.figure(figsize=(12, 8))
    plt.plot(signals['cumulative_returns'], label='Cumulative Returns', color='blue')
    plt.title('Cumulative Returns - Simple Moving Average Strategy')
    plt.legend()
    plt.show()
    
    return signals

sma_signals = SMA_strategy(data)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





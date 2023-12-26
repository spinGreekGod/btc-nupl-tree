import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Data
btc = yf.download('BTC-USD', start='2010-01-01', end='2023-12-25', interval='1d')

#FE
btc['NUPL'] = (btc['Close'] - btc['Close'].rolling(window=200).mean()) / btc['Close'].rolling(window=200).mean()
btc['NUPL'] = btc['NUPL'].fillna(0)  # Replace NaN values with 0 for the beginning

# Hash Ribbons Features using Moving Averages
btc['SMA_30'] = btc['Close'].rolling(window=30).mean()
btc['SMA_60'] = btc['Close'].rolling(window=60).mean()


btc['Hash_Ribbons_Feature_1'] = np.where(btc['SMA_30'] > btc['SMA_60'], 1, 0)
btc['Hash_Ribbons_Feature_2'] = np.where(btc['SMA_30'] < btc['SMA_60'], 1, 0)

# Define conditions for long and short positions based on NUPL
btc['Long_Position'] = np.where(btc['NUPL'] > 0, btc['Close'], np.nan)
btc['Short_Position'] = np.where(btc['NUPL'] < 0, btc['Close'], np.nan)

# Plotting
plt.figure(figsize=(12, 6))

# Plotting Price
plt.plot(btc.index, btc['Close'], label='Price')


plt.scatter(btc.index, btc['Long_Position'], color='green', marker='^', label='Long', alpha=0.7)
plt.scatter(btc.index, btc['Short_Position'], color='red', marker='v', label='Short', alpha=0.7)


plt.plot(btc.index, btc['SMA_30'], '--', label='SMA 30')
plt.plot(btc.index, btc['SMA_60'], '--', label='SMA 60')

plt.yscale('log')  
plt.title('Price, Long/Short Positions, and Hash Ribbons Features')
plt.xlabel('Date')
plt.ylabel('Value (Log Scale)')
plt.legend()
plt.grid()
plt.show()

import pandas as pd
import numpy as np
import yfinance
from mpl_finance import candlestick_ohlc
import warnings
warnings.filterwarnings("ignore")
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import ccxt
import config
import json
import time




TRADESYMBOL ='ICP/USDT'
    
def supportzones(price,TRADESYMBOL):
  plt.rcParams['figure.figsize'] = [12, 7]
  plt.rc('font', size=14)
  with open("symbols.json", "r") as f:
    TRADE = json.load(f)
    TRADESYMBOL = TRADE[TRADESYMBOL]
    f.close()
    
  name = TRADESYMBOL +'-USD'
  ticker = yfinance.Ticker(name)
  
  df = ticker.history(interval="1h",start="2021-06-10", end="2021-06-18")
  print (df)
  print('********* compare it to the next one ********')
  df['Date'] = pd.to_datetime(df.index)
  df['Date'] = df['Date'].apply(mpl_dates.date2num)
  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

  def isSupport(df,i):
      support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
      return support
  def isResistance(df,i):
    resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
    return resistance

  levels = []
  for i in range(2,df.shape[0]-2):
    if isSupport(df,i):
      levels.append((i,df['Low'][i]))
    elif isResistance(df,i):
      levels.append((i,df['High'][i]))
      
  def plot_all():
    fig, ax = plt.subplots()
    candlestick_ohlc(ax,df.values,width=0.01, \
                    colorup='green', colordown='red', alpha=0.7)
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    fig.suptitle(f' {name} Chart', fontsize=16)
    fig.tight_layout()
    for level in levels:
      plt.hlines(level[1],xmin=df['Date'][level[0]],\
                xmax=max(df['Date']),colors='blue')
    fig.show()

    plt.show()
    
  s =  np.mean(df['High'] - df['Low'])

  def isFarFromLevel(l):
      return np.sum([abs(l-x) < s  for x in levels]) == 0

  levels = []
  for i in range(2,df.shape[0]-2):
    if isSupport(df,i):
      l = df['Low'][i]

      if isFarFromLevel(l):
        levels.append((i,l))

    elif isResistance(df,i):
      l = df['High'][i]

      if isFarFromLevel(l):
        levels.append((i,l))
  rs = []
  for level in levels :
      # print(level[1]) 
      rs.append(level[1])
  rs.sort(reverse=True)

  # print(rs)
  x = rs
  zones = []
  k = 0
  for k in range(len(x)-1):
    marge = [x[k],x[k+1]]
    # print(k)
    zones.append(marge)
  # print(zones)
  # print('******************* Zone test ********')
  price = price
  for zone in zones:
    if (price < zone[0]) and (price > zone[1]) :
      # print ('This is true')
      # print(zone[0],zone[1])
      z = abs(zones.index(zone)-len(zones))
      print(f' This is zone {z}')

    # elif price >zone[0] :
    #   z =77
    # elif price <zone[1] :
    #   z = 55
  
    else :
          z = 51
  print(f'This zone is : {z}')
  plot_all()
  return z 




# ? SAfe Zone Function 





def Safezone(price,TRADESYMBOL):
  plt.rcParams['figure.figsize'] = [12, 7]
  plt.rc('font', size=14)
  with open("symbols.json", "r") as f:
    TRADE = json.load(f)
    TRADESYMBOL = TRADE[TRADESYMBOL]
    f.close()
  name = TRADESYMBOL+'-USD'
  ticker = yfinance.Ticker(name)
  df = ticker.history(interval="1h",start="2021-06-10", end="2021-06-18")
  df['Date'] = pd.to_datetime(df.index)
  df['Date'] = df['Date'].apply(mpl_dates.date2num)
  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

  def isSupport(df,i):
      support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
      return support
  def isResistance(df,i):
    resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
    return resistance

  levels = []
  for i in range(2,df.shape[0]-2):
    if isSupport(df,i):
      levels.append((i,df['Low'][i]))
    elif isResistance(df,i):
      levels.append((i,df['High'][i]))
      
  def plot_all():
    fig, ax = plt.subplots()
    candlestick_ohlc(ax,df.values,width=0.01, \
                    colorup='green', colordown='red', alpha=0.7)
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    fig.suptitle(f' {name} Chart', fontsize=16)
    fig.tight_layout()
    for level in levels:
      plt.hlines(level[1],xmin=df['Date'][level[0]],\
                xmax=max(df['Date']),colors='blue')
    fig.show()

    plt.show()
    
  s =  np.mean(df['High'] - df['Low'])

  def isFarFromLevel(l):
      return np.sum([abs(l-x) < s  for x in levels]) == 0

  levels = []
  for i in range(2,df.shape[0]-2):
    if isSupport(df,i):
      l = df['Low'][i]

      if isFarFromLevel(l):
        levels.append((i,l))

    elif isResistance(df,i):
      l = df['High'][i]

      if isFarFromLevel(l):
        levels.append((i,l))
  rs = []
  for level in levels :
      # print(level[1]) 
      rs.append(level[1])
  rs.sort(reverse=True)

  # print(rs)
  x = rs
  zones = []
  k = 0
  for k in range(len(x)-1):
    marge = [x[k],x[k+1]]
    # print(k)
    zones.append(marge)
  print(zones)
  price = price
  for zone in zones:
    if (price < zone[0]) and (price > zone[1]) :
      # print ('This is true')
      # print(zone[0],zone[1])
      z = abs(zones.index(zone)-len(zones))
      print(f' This is zone {z}')
      if z < len(zones)/2 :
        safe = True
        print('This is a Safe zone')
      elif z > len(zones)/2  :
        safe = False
        print('This is a Volat Zone')
    else :
      safe = False

  # plot_all()
  time.sleep(3)
  print(f'This zone is {safe}')
  return safe

supportzones(150,'LTC/USDT')


print(f'this is the zone {supportzones(23.8,TRADESYMBOL)} and safe = {Safezone(23.8,TRADESYMBOL)}')
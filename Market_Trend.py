
import datetime
from pandas._libs.tslibs import Timestamp
import websocket, json, pprint, talib,numpy
import config
from binance.client import Client
from binance.enums import *
import pandas as pd 
pd.set_option('display.max_rows',None)
import warnings
warnings.filterwarnings('ignore')
import ta
import ccxt
import schedule
from ta.volatility import AverageTrueRange, BollingerBands
import time
from termcolor import colored
from colorama import Fore, Back, Style,init
init()


def Market_Trend(TRADE_SYMBOL,time,limit):
    
    exchange_id = 'binance'
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': config.API_KEY,
        'secret': config.API_SECRET,
        'timeout': 30000,
        'enableRateLimit': True,
    })
    
    print(Fore.GREEN+f"Fetching new Bars for {TRADE_SYMBOL} AT {datetime.datetime.now().isoformat()}")
    bars_ST = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe=time, limit=limit)
    df_ST = pd.DataFrame(bars_ST, columns=['timestamp','open','high','low','close','volume'])
    df_ST['timestamp'] = pd.to_datetime(df_ST['timestamp'],unit='ms')


    def TR(df_ST):
            df_ST['previous_close'] = df_ST['close'].shift(1)
            df_ST['high-low'] = df_ST['high'] - df_ST['low']
            df_ST['high-pc'] = abs(df_ST['high'] - df_ST['previous_close'])
            df_ST['low-pc'] = abs(df_ST['low'] - df_ST['previous_close'])
            tr = df_ST[['high-low', 'high-pc', 'low-pc']].max(axis=1)
            return tr


    def atr (df_ST, period):
        df_ST['tr'] = TR(df_ST)
        the_atr = df_ST['tr'].rolling(period).mean()
        #df_ST['atr'] = the_atr
        #print(df)
        return the_atr



    def supertrend(df_ST,period=7,multiplier=3):
            print(colored('Calculating SuperTrend','green'))
            df_ST['atr'] = atr(df_ST,period=period)
            df_ST['upperband'] = ((df_ST['high'] + df_ST['low'])/2) + (multiplier * df_ST['atr'])
            df_ST['lowerband'] =  ((df_ST['high'] + df_ST['low'])/2) - (multiplier * df_ST['atr'])
            df_ST['in_uptrend'] = True
            
            for current in range (1, len(df_ST.index)):
                previous = current - 1
                if df_ST['close'][current] > df_ST['upperband'] [previous]:
                    df_ST['in_uptrend'][current] = True
                elif df_ST['close'][current] < df_ST['lowerband'][previous]:
                    df_ST['in_uptrend'][current] = False
                else :
                    df_ST['in_uptrend'][current] = df_ST['in_uptrend'][previous]
                    
                    if df_ST['in_uptrend'][current] and df_ST['lowerband'][current]< df_ST['lowerband'][previous]:
                        df_ST['lowerband'][current] = df_ST['lowerband'][previous]
                    
                    if not df_ST['in_uptrend'][current] and df_ST['upperband'][current]>df_ST['upperband'][previous]:
                        df_ST['upperband'][current] = df_ST['upperband'][previous]
                
            
            return df_ST
        
    
    analyse = supertrend(df_ST)
    return analyse
    
        
    
    
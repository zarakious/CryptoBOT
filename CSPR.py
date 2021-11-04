#*Candlestick Pattern Recognition
from numpy import fabs
import config
import ccxt
import pandas as pd
import talib
from patty import patterns

exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': config.API_KEY,
    'secret': config.API_SECRET,
    'timeout': 80000,
    'recvWindow': 10000000,
    'enableRateLimit': True,
})

def pattern_detector(TRADE_SYMBOL,timeframe):
    Bars = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe=timeframe, limit=48)
    DF_CSPR = pd.DataFrame(Bars[:-1], columns=['timestamp','open','high','low','close','volume'])
    DF_CSPR['timestamp'] = pd.to_datetime(DF_CSPR['timestamp'],unit='ms')
    for pattern in patterns:
        pattern_function = getattr(talib,pattern)
        result = pattern_function(DF_CSPR['open'], DF_CSPR['high'], DF_CSPR['low'], DF_CSPR['close'])
        DF_CSPR[pattern] = result
    last = DF_CSPR.tail(1).values
    if 100 in last  and -100 not in last:
        print ("Uptend Signal Found !!!!")
        print(last)
        return True
    else :
        return False
    






           




# engulfing_days = DF_CSPR[DF_CSPR['ENGULFING']!=0]
# morning_days = DF_CSPR[DF_CSPR['Morning_STAR']!=0]

#print(DF_CSPR)





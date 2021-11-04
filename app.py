import config
from flask import Flask, render_template,request
from patterns import patterns 
import pandas as pd
import ccxt
import talib
import stocks

app = Flask(__name__)
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': config.API_KEY,
    'secret': config.API_SECRET,
    'timeout': 30000,
    'enableRateLimit': True,
})
@app.route('/')
def index():
    pattern = request.args.get('pattern',None)
    stocks = ['ICP/USDT','BNB/USDT','LTC/USDT','ETH/BTC','LTC/BNB','XRP/USDT']
            
    


    if pattern:
        print(pattern)
        bars_ST = exchange.fetch_ohlcv('BTC/USDT',timeframe='1d', limit=1000)
        df_ST = pd.DataFrame(bars_ST[:-1], columns=['timestamp','open','high','low','close','volume'])
        df_ST['timestamp'] = pd.to_datetime(df_ST['timestamp'],unit='ms')
        pattern_function = getattr(talib,pattern)
        result  = pattern_function(df_ST['open'], df_ST['high'], df_ST['low'], df_ST['close'])
        last = result.tail(1).values[0]
        if last != 0:
            print('founddddddddddd')
            print(last)
        else :
            print(f'No {pattern} detetcted !!!')
            print(result)
        #print(df_ST)
       
        
    return render_template('index.html',patterns=patterns,stocks=stocks,pattern=pattern)

@app.route('/snapshot')
def snapshot():
    return('this is a fck oupi ')
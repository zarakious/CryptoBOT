#Importing the modules 

from datetime import datetime
import datetime
import time
from pandas._libs.tslibs import Timestamp
import talib
import config
from binance.enums import *
import pandas as pd 
import json
import support
pd.set_option('display.max_rows',None)
import warnings
warnings.filterwarnings('ignore')
import ccxt
from ta.volatility import AverageTrueRange, BollingerBands
from termcolor import colored
import CSPR
import yoda
import urllib.request, json 

from colorama import Fore, Back, Style,init
init()


RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TP =  1.3
SL = 10
TRADE_QUANTITY = 0.10
STOCH_RSI = 12
#order_buy_price = 0
#order_sell_price = 0
#closes = []  
with open("in_position.json", "r") as f:
    in_position = json.load(f)
with open("order_buy_price.json", "r") as f:
    order_buy_price = json.load(f)
with open("in_position.json", "r") as f:
    order_sell_price = json.load(f)



def Bot_trader(TRADE_SYMBOL,DURATION):
    
    # client = Client(config.API_KEY, config.API_SECRET, tld='us')

    # *Binance Account

    exchange_id = 'binance'
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': config.API_KEY,
        'secret': config.API_SECRET,
        #'timeout': 80000,
        'enableRateLimit': True
    })


    # *BollingerBands Analyse
    def bbands() :

        bars = exchange.fetch_ohlcv(TRADE_SYMBOL,limit=21)

        df = pd.DataFrame(bars[:-1], columns=['timestamp','open','high','low','close','volume'])

        bb_indicator = BollingerBands(df['close'])
        df['upper_band'] = bb_indicator.bollinger_hband()
        BB_Upperband = df['upper_band'][19]
        df['Lower_band'] = bb_indicator.bollinger_lband()
        BB_Lowerband = df['Lower_band'][19]
        df['moving_average'] = bb_indicator.bollinger_mavg()
        atr_indicator = AverageTrueRange(df['high'],df['low'],df['close'])
        df['atr'] = atr_indicator.average_true_range()
        Last_kundle = df['close'][19]
        print(colored('The Value of the Last Kundle is : ','white')+colored(Last_kundle,'blue'))
        print(colored('The Value of the Upper BBANDS is : ','white')+colored(BB_Upperband,'green'))
        print(colored('The Value of the Lower BBANDS is : ','white')+colored(BB_Lowerband,'red'))
        if Last_kundle > BB_Upperband:
            print(colored('****Attention*** There is an intersection with the Upper Band !','green'))
            return 1
        elif Last_kundle < BB_Lowerband :
            print(colored('****Attention*** There is an intersection with the Lower Band !','red'))
            return 0
        else :
            return 3
            
    #* RSI Detector 
    def Rsi_Calculator():
        bars_rsi = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe='3m', limit=500)
        df_rsi = pd.DataFrame(bars_rsi, columns=['timestamp','open','high','low','close','volume'])
        RSI = (talib.RSI(df_rsi['close'],RSI_PERIOD))[499]
        Earlier_RSI = (talib.RSI(df_rsi['close'],RSI_PERIOD))[498]
        #MA_7 = (talib.SMA(df_rsi['close'],7))[28]
        #MA_25 = (talib.SMA(df_rsi['close'],25))[28]
        # print(f'The Eralier RSI : {Earlier_RSI}')
        # print(f'The Previous RSI : {Previous_RSI}')
        
        print(f'The Current RSI for {TRADE_SYMBOL}  is {RSI}')
        print(f'The previous RSI VALUE is : {Earlier_RSI}')
        print('***********************************************************************')
        return Earlier_RSI
    
    def EMA_Calculator():
        bars_rsi = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe='3m', limit=500)
        df_rsi = pd.DataFrame(bars_rsi, columns=['timestamp','open','high','low','close','volume'])
        EMA_5 = (talib.EMA(df_rsi['close'],5))[499]
        EMA_8 = (talib.EMA(df_rsi['close'],8))[499]
        EMA_13 =(talib.EMA(df_rsi['close'],13))[499]
        PREVIOUS_EMA_5 = (talib.EMA(df_rsi['close'],6))[498]
        PREVIOUS_EMA_8 = (talib.EMA(df_rsi['close'],14))[498]
        PREVIOUS_EMA_13 = (talib.EMA(df_rsi['close'],26))[498]
        
        print(f'The Current EMA_5 for {TRADE_SYMBOL}  is {EMA_5}')
        print(f'The previous EMA VALUE is : {PREVIOUS_EMA_5}')
        KUNDLE_1 = df_rsi['close'][498]
        KUNDLE_2 = df_rsi['close'][497]
        KUNDLE_3 = df_rsi['close'][496]
        print(f'Last KUNDLE {KUNDLE_1}')
        print(f'Previous KUNDLE {KUNDLE_2}')
        print(f'Earlier Kundle {KUNDLE_3}')
        # if (KUNDLE_3 < PREVIOUS_EMA_5) and (KUNDLE_2 < PREVIOUS_EMA_5) and (KUNDLE_1 > PREVIOUS_EMA_5):
        if ((PREVIOUS_EMA_5 > PREVIOUS_EMA_8) and (PREVIOUS_EMA_8 > PREVIOUS_EMA_13) and (KUNDLE_1 > PREVIOUS_EMA_5))\
            and KUNDLE_2 < PREVIOUS_EMA_5:
                # or ((KUNDLE_3 < PREVIOUS_EMA_5) and (KUNDLE_3 < PREVIOUS_EMA_8))) :
                
            print('BUY SIGNAL BASED ON EMA ')
            BUY_SIGNAL = True
        else :
            print('NO BUY SIGNAL BASED ON EMA ')
            BUY_SIGNAL = False
        return BUY_SIGNAL
    def is_MACD():
        bars_rsi = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe='3m', limit=500)
        df_rsi = pd.DataFrame(bars_rsi, columns=['timestamp','open','high','low','close','volume'])
        # EMA_5 = (talib.EMA(df_rsi['close'],5))[499]
        # EMA_8 = (talib.EMA(df_rsi['close'],8))[499]
        # EMA_13 =(talib.EMA(df_rsi['close'],13))[499]
        PREVIOUS_EMA_5 = (talib.EMA(df_rsi['close'],6))[498]
        PREVIOUS_EMA_8 = (talib.EMA(df_rsi['close'],14))[498]
        PREVIOUS_EMA_13 = (talib.EMA(df_rsi['close'],26))[498]
        PREVIOUS_EMA_200 = (talib.EMA(df_rsi['close'],200))[498]
        Kundle1 = df_rsi['close'][498]
        
        macd, macdsignal, macdhist = talib.MACD(df_rsi['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        # macdsignal= talib.MACD(df_rsi, fastperiod=12, slowperiod=26, signalperiod=9)
        # macdhist = talib.MACD(df_rsi, fastperiod=12, slowperiod=26, signalperiod=9)
        # print (f'this is macd : {macd[498]}')
        # print(f'this is macdsignal : {macdsignal[498]}')
        # print(f'This is  macdhist {macdhist[498]}')        

        # if (KUNDLE_3 < PREVIOUS_EMA_5) and (KUNDLE_2 < PREVIOUS_EMA_5) and (KUNDLE_1 > PREVIOUS_EMA_5):
        if ((PREVIOUS_EMA_5 > PREVIOUS_EMA_8) and (macd[498]>macdsignal[498]) and (macd[498]<0)) and (PREVIOUS_EMA_200 < Kundle1) :   
            print('BUY SIGNAL BASED ON MACD ')
            BUY_SIGNAL = True
        else :
            print('NO BUY SIGNAL BASED ON MACD ')
            BUY_SIGNAL = False
        return BUY_SIGNAL
    
    
    def EMA_5M():
        bars_rsi = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe='5m', limit=500)
        df_rsi = pd.DataFrame(bars_rsi, columns=['timestamp','open','high','low','close','volume'])

        PREVIOUS_EMA_5 = (talib.EMA(df_rsi['close'],5))[499]
        PREVIOUS_EMA_8 = (talib.EMA(df_rsi['close'],8))[499]
        PREVIOUS_EMA_13 = (talib.EMA(df_rsi['close'],13))[499]
        
        # print(f'The Current EMA_5 for {TRADE_SYMBOL}  is {EMA_5}')
        print(f'The previous EMA VALUE is : {PREVIOUS_EMA_5}')
        KUNDLE_1 = df_rsi['close'][498]
        KUNDLE_2 = df_rsi['close'][497]
        KUNDLE_3 = df_rsi['close'][496]
        print(f'Last KUNDLE {KUNDLE_1}')
        print(f'Previous KUNDLE {KUNDLE_2}')
        print(f'Earlier Kundle {KUNDLE_3}')
        # if (KUNDLE_3 < PREVIOUS_EMA_5) and (KUNDLE_2 < PREVIOUS_EMA_5) and (KUNDLE_1 > PREVIOUS_EMA_5):
        if ((PREVIOUS_EMA_5 > PREVIOUS_EMA_8) and (PREVIOUS_EMA_8 > PREVIOUS_EMA_13) ):
            
                # or ((KUNDLE_3 < PREVIOUS_EMA_5) and (KUNDLE_3 < PREVIOUS_EMA_8))) :
                
            print('BUY SIGNAL BASED ON EMA_5M ')
            BUY_SIGNAL = True
        else :
            print('NO BUY SIGNAL BASED ON EMA_5M ')
            BUY_SIGNAL = False
        return BUY_SIGNAL
    
    
    def EMA_15M():
        bars_rsi = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe='15m', limit=500)
        df_rsi = pd.DataFrame(bars_rsi, columns=['timestamp','open','high','low','close','volume'])

        PREVIOUS_EMA_5 = (talib.EMA(df_rsi['close'],5))[499]
        PREVIOUS_EMA_8 = (talib.EMA(df_rsi['close'],8))[499]
        PREVIOUS_EMA_13 = (talib.EMA(df_rsi['close'],13))[499]
        
        # print(f'The Current EMA_5 for {TRADE_SYMBOL}  is {EMA_5}')
        print(f'The previous EMA VALUE is : {PREVIOUS_EMA_5}')
        KUNDLE_1 = df_rsi['close'][498]
        KUNDLE_2 = df_rsi['close'][497]
        KUNDLE_3 = df_rsi['close'][496]
        print(f'Last KUNDLE {KUNDLE_1}')
        print(f'Previous KUNDLE {KUNDLE_2}')
        print(f'Earlier Kundle {KUNDLE_3}')
        # if (KUNDLE_3 < PREVIOUS_EMA_5) and (KUNDLE_2 < PREVIOUS_EMA_5) and (KUNDLE_1 > PREVIOUS_EMA_5):
        if ((PREVIOUS_EMA_5 > PREVIOUS_EMA_8) and (PREVIOUS_EMA_8 > PREVIOUS_EMA_13) ):
            
                # or ((KUNDLE_3 < PREVIOUS_EMA_5) and (KUNDLE_3 < PREVIOUS_EMA_8))) :
                
            print('BUY SIGNAL BASED ON EMA_15M ')
            BUY_SIGNAL = True
        else :
            print('NO BUY SIGNAL BASED ON EMA_15M ')
            BUY_SIGNAL = False
        return BUY_SIGNAL
    
    def is_correct():
        if EMA_5M() == True and EMA_15M == True :
            return True
        else :
            return False
        
    
    #* Calculate STOCH
    
    def CURRENT_STOCH ():
        bars_rsi = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe='3m', limit=100)
        df_rsi = pd.DataFrame(bars_rsi[:-1], columns=['timestamp','open','high','low','close','volume'])
        fastk, fastd = talib.STOCHRSI(df_rsi['close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        tx = fastk
        lx = fastd
        return lx[27],lx[28]
        

    #* Calculate The current_price (MA)

    def current_price():
        bars_price = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe='1m',limit=30)
        df_price = pd.DataFrame(bars_price, columns=['timestamp','open','high','low','close','volume'])
        current_price = df_price['close'][29]
        print(f'The Current price is {current_price}')
        return current_price
        
        

    def price_now():
        trade = TRADE_SYMBOL.replace("/","")
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={trade}'
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            print('The current price with json is :')
            print(data)

    ## *SuperTrend Detector


    def TR(df_ST):
        df_ST['previous_close'] = df_ST['close'].shift(1)
        df_ST['high-low'] = df_ST['high'] - df_ST['low']
        df_ST['high-pc'] = abs(df_ST['high'] - df_ST['previous_close'])
        df_ST['low-pc'] = abs(df_ST['low'] - df_ST['previous_close'])
        tr = df_ST[['high-low', 'high-pc', 'low-pc']].max(axis=1)
        return tr


    def atr (df_ST, period):
        df_ST['tr'] = TR(df_ST)
        print(colored('Calculate average true range (ATR)','yellow'))
        the_atr = df_ST['tr'].rolling(period).mean()
        #df_ST['atr'] = the_atr
        #print(df)
        return the_atr

    def supertrend(df_ST,period=7,multiplier=3):
        # bbands()
        current_price()
        print(colored('Calculating SuperTrend','blue'))
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
    
    
    
    #? TREND ANND SUPERTREND
    
    
    # def TREND (DF_TREND):
    #     print('helllo')
    #     DF_TREND['in_uptrend'] = True
    #     for current in range (1, len(DF_TREND.index)):
    #         previous = current - 1
    #         if DF_TREND['close'][current] > DF_TREND['close'] [previous]:
    #             DF_TREND['in_uptrend'][current] = True
    #         elif DF_TREND['close'][current] < DF_TREND['close'][previous]:
    #             DF_TREND['in_uptrend'][current] = False
            
    #     print(DF_TREND.tail(4))
    #     return DF_TREND

    #****Calculating RSI******

    # def check_RSI(df_ST):
    #     np_closes = numpy.array(closes)
    #     last_close = df_ST['close'].tail(1)
    #     closes.append(float(last_close))
    #     if len(closes)> RSI_PERIOD:
    #         rsi = talib.RSI(np_closes, RSI_PERIOD)
    #         print(f'The Current RSI is {rsi}')
    #     else:
    #         print('still calculating....')


    def check_buy_sell_signals (df_ST):
        global in_position
        global order_sell_price
        global order_buy_price
        # BUY_SIGNAL = detetctor.pattern_detector(TRADE_SYMBOL,'15m')
        print(f'In postion = {in_position[TRADE_SYMBOL]}')
    
        # print(f'The current Stoch RSI : {CURRENT_STOCH()}')
        
        # print(f'The current trade zone is {support.supportzones(current_price(),TRADE_SYMBOL)}')
        # print(f'The current trade zone is {support.Safezone(current_price(),TRADE_SYMBOL)}')
        print (colored("Checking for Buy and sell Signals",'white'))
        # safe = support.Safezone(current_price(),TRADE_SYMBOL)
        #Rsi_Calculator()
        print(colored(df_ST.tail(2),'blue'))
        last_row_index = len(df_ST.index) - 1
        previous_row_index = last_row_index - 1
        is_MACD()
        # TREND_last_row_index = len(TREND_DATA.index) - 1
        # TREND_previous_row_index = TREND_last_row_index - 1
        
        
        # if (not df_ST['in_uptrend'][previous_row_index] and df_ST['in_uptrend'][last_row_index] )\
        # if (not TREND_DATA['in_uptrend'][previous_row_index] and TREND_DATA['in_uptrend'][last_row_index] )\
        if (EMA_Calculator() == True and is_correct()== True) or (is_MACD() == True) or (not df_ST['in_uptrend'][previous_row_index] and df_ST['in_uptrend'][last_row_index] ):
        # or  (Rsi_Calculator()< RSI_OVERSOLD) or EMA_Calculator() ==True :
            # if Rsi_Calculator() < RSI_OVERSOLD :
            print("Changed To Uptrend ! Checking For buying OPP")
            dateTimeObj = datetime.datetime.now()
            if (not in_position[TRADE_SYMBOL]) :
                #order= exchange.create_market_buy_order('ICP/USDT', 0.1)
                order = 'We Executed A buy Order'
                print(order)
                with open("in_position.json", "r+") as f:
                    in_position = json.load(f)
                    in_position[TRADE_SYMBOL] = True
                    f.seek(0)  # rewind
                    f.truncate()
                    json.dump(in_position, f)
                    f.truncate()
                    f.close()
                with open("order_buy_price.json", "r+") as f:
                    order_buy_price[TRADE_SYMBOL] = current_price()
                    json.dump(order_buy_price, f)
                    f.close()
                print(order_buy_price[TRADE_SYMBOL])
                
                file1 = open("deals.txt","a")
                file1.write(str(f'{dateTimeObj} => We bought the {TRADE_SYMBOL} at {order_buy_price[TRADE_SYMBOL]} USDT'))
                file1.write("\n")
                file1.close
                yoda.send_message(str(f'\U00002934 \U00002934 \U00002934 \U00002934 Buy Signal {TRADE_SYMBOL} at {order_buy_price[TRADE_SYMBOL]} USDT !!!\n \
                     \U00002733 \U00002733'))
                # os.system('say "Trade Made."')
                
            else :
                print("We are already in position just wait Dude  !")

        
        if in_position[TRADE_SYMBOL] :
            if (current_price() > order_buy_price[TRADE_SYMBOL] + ((order_buy_price[TRADE_SYMBOL]*TP/100)) ):
                # or (Rsi_Calculator() > RSI_OVERBOUGHT) and (current_price() > order_buy_price[TRADE_SYMBOL]) :
                
                print("Changed to downtrend ! Sell")
                #order = exchange.create_market_sell_order('ICP/USDT', 0.1)
                order_sell = 'The sell order is done with succes '
                print(order_sell)
                order_sell_price[TRADE_SYMBOL] = current_price()
                print (f'we bought the order at {order_buy_price[TRADE_SYMBOL]} and we sell it for {order_sell_price[TRADE_SYMBOL]} and we made {order_sell_price[TRADE_SYMBOL]-order_buy_price[TRADE_SYMBOL]} USDT')
                file1 = open("deals.txt","a")
                file1.write(str(f'we bought the order({TRADE_SYMBOL}) at {order_buy_price[TRADE_SYMBOL]} and we sell it for {order_sell_price[TRADE_SYMBOL]} and we made {order_sell_price[TRADE_SYMBOL]-order_buy_price[TRADE_SYMBOL]} USDT'))
                file1.write("\n")
                file1.close
                in_position[TRADE_SYMBOL] = False
                with open("in_position.json", "r+") as f:
                    in_position = json.load(f)
                    in_position[TRADE_SYMBOL] = False
                    f.seek(0)  # rewind
                    f.truncate()
                    json.dump(in_position, f)
                    f.truncate()
                    f.close()
                    yoda.send_message(str(f'\U00002714 \U00002714 \U00002714 \U00002728 \U00002728 \U00002728 We bought the order({TRADE_SYMBOL}) for {order_buy_price[TRADE_SYMBOL]} and we sell it for {order_sell_price[TRADE_SYMBOL]} and we made {order_sell_price[TRADE_SYMBOL]-order_buy_price[TRADE_SYMBOL]} USDT  \U00002764 \U00002764 \U00002764 \U00002764 \U00002764  {TP}%'))
                    
                    
            elif in_position[TRADE_SYMBOL] and (current_price() < order_buy_price[TRADE_SYMBOL] ):
                print("You are in Position But we keep looking for better price ! ")

            
            else: 
                print ("We are Free Nothing to do !")

        
    def run_bot():
        print(Fore.BLUE+f"Fetching new Bars for {datetime.datetime.now().isoformat()}......")
        bars_ST = exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe='1h', limit=100)
        # bars_TREND =  exchange.fetch_ohlcv(TRADE_SYMBOL,timeframe='1h', limit=100)
        df_ST = pd.DataFrame(bars_ST[:-1], columns=['timestamp','open','high','low','close','volume'])
        df_ST['timestamp'] = pd.to_datetime(df_ST['timestamp'],unit='ms')
        # DF_TREND = pd.DataFrame(bars_TREND[:-1], columns=['timestamp','open','high','low','close','volume'])
        # DF_TREND['timestamp']  = pd.to_datetime(DF_TREND['timestamp'],unit='ms')
        #print(df_ST)
        supertrend_data =  supertrend(df_ST)
        # TREND_DATA = TREND(DF_TREND)
        check_buy_sell_signals(supertrend_data)
        
    return run_bot()
        








































# # ** RSI n Order 
# def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
#     try:
#         print("sending order")
#         order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
#         print(order)
#     except Exception as e:
#         print("an exception occured - {}".format(e))
#         return False

#     return True
 
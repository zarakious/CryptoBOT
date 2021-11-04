# #Importing the modules 

# import datetime
# from pandas._libs.tslibs import Timestamp
# import websocket, json, pprint, talib,numpy
# import config
# from binance.client import Client
# from binance.enums import *
# import pandas as pd 
# pd.set_option('display.max_rows',None)
# import warnings
# warnings.filterwarnings('ignore')
# import ta
# import ccxt
# import schedule
# from ta.volatility import AverageTrueRange, BollingerBands
# import time
# from termcolor import colored
# from colorama import Fore, Back, Style,init
# init()



# # The Soket is declared here


# SOCKET = "wss://stream.binance.com:9443/ws/icpusdt@kline_1m"

# RSI_PERIOD = 14
# RSI_OVERBOUGHT = 75
# RSI_OVERSOLD = 33
# TRADE_SYMBOL = 'ICPUSDT'
# TRADE_QUANTITY = 0.10
# order_buy_price = 140
# order_sell_price = 0
# closes = []
# in_position = False

# client = Client(config.API_KEY, config.API_SECRET, tld='us')


# # *Binance Account

# exchange_id = 'binance'
# exchange_class = getattr(ccxt, exchange_id)
# exchange = exchange_class({
#     'apiKey': config.API_KEY,
#     'secret': config.API_SECRET,
#     'timeout': 30000,
#     'enableRateLimit': True,
# })


# # *BollingerBands Analyse
# def bbands() :

#     bars = exchange.fetch_ohlcv('ICP/USDT',limit=21)

#     df = pd.DataFrame(bars[:-1], columns=['timestamp','open','high','low','close','volume'])

#     bb_indicator = BollingerBands(df['close'])
#     df['upper_band'] = bb_indicator.bollinger_hband()
#     BB_Upperband = df['upper_band'][19]
#     df['Lower_band'] = bb_indicator.bollinger_lband()
#     BB_Lowerband = df['Lower_band'][19]
#     df['moving_average'] = bb_indicator.bollinger_mavg()
#     atr_indicator = AverageTrueRange(df['high'],df['low'],df['close'])
#     df['atr'] = atr_indicator.average_true_range()
#     Last_kundle = df['close'][19]
#     print(colored('The Value of the Last Kundle is : ','white')+colored(Last_kundle,'blue'))
#     print(colored('The Value of the Upper BBANDS is : ','white')+colored(BB_Upperband,'green'))
#     print(colored('The Value of the Lower BBANDS is : ','white')+colored(BB_Lowerband,'red'))
#     if Last_kundle > BB_Upperband:
#         print(colored('****Attention*** There is an intersection with the Upper Band !','green'))
#         return 1
#     elif Last_kundle < BB_Lowerband :
#         print(colored('****Attention*** There is an intersection with the Lower Band !','red'))
#         return 0
#     else :
#         return 3
        
# #* RSI Detector 
# def Rsi_Calculator():
#     bars_rsi = exchange.fetch_ohlcv('ICP/USDT',limit=30)
#     df_rsi = pd.DataFrame(bars_rsi[:-1], columns=['timestamp','open','high','low','close','volume'])
#     RSI = (talib.RSI(df_rsi['close'],RSI_PERIOD))[28]
#     Previous_RSI = (talib.RSI(df_rsi['close'],RSI_PERIOD))[27]
#     Earlier_RSI = (talib.RSI(df_rsi['close'],RSI_PERIOD))[26]
#     MA_7 = (talib.SMA(df_rsi['close'],7))[28]
#     MA_25 = (talib.SMA(df_rsi['close'],25))[28]
#     # print(f'The Eralier RSI : {Earlier_RSI}')
#     # print(f'The Previous RSI : {Previous_RSI}')
#     print(f'The Current RSI : {RSI}')
#     print(f'The moving average (MA7) : {MA_7}')
#     print(f'The moving average (MA25) : {MA_25}')
#     return RSI

# #* Calculate The current_price (MA)

# def current_price():
#     bars_price = exchange.fetch_ohlcv('ICP/USDT',limit=30)
#     df_price = pd.DataFrame(bars_price, columns=['timestamp','open','high','low','close','volume'])
#     current_price = df_price['close'][28]
#     print(f'The Current price is {current_price}')
#     return current_price
    



# ## *SuperTrend Detector

# echange_ST = ccxt.binanceus()

# def TR(df_ST):
#     df_ST['previous_close'] = df_ST['close'].shift(1)
#     df_ST['high-low'] = df_ST['high'] - df_ST['low']
#     df_ST['high-pc'] = abs(df_ST['high'] - df_ST['previous_close'])
#     df_ST['low-pc'] = abs(df_ST['low'] - df_ST['previous_close'])
#     tr = df_ST[['high-low', 'high-pc', 'low-pc']].max(axis=1)
#     return tr


# def atr (df_ST, period):
#     df_ST['tr'] = TR(df_ST)
#     print(colored('Calculate average true range (ATR)','yellow'))
#     the_atr = df_ST['tr'].rolling(period).mean()
#     #df_ST['atr'] = the_atr
#     #print(df)
#     return the_atr

# def supertrend(df_ST,period=7,multiplier=3):
#     bbands()
#     current_price()
#     print(colored('Calculating SuperTrend','green'))
#     df_ST['atr'] = atr(df_ST,period=period)
#     df_ST['upperband'] = ((df_ST['high'] + df_ST['low'])/2) + (multiplier * df_ST['atr'])
#     df_ST['lowerband'] =  ((df_ST['high'] + df_ST['low'])/2) - (multiplier * df_ST['atr'])
#     df_ST['in_uptrend'] = True
    
#     for current in range (1, len(df_ST.index)):
#         previous = current - 1
#         if df_ST['close'][current] > df_ST['upperband'] [previous]:
#             df_ST['in_uptrend'][current] = True
#         elif df_ST['close'][current] < df_ST['lowerband'][previous]:
#             df_ST['in_uptrend'][current] = False
#         else :
#             df_ST['in_uptrend'][current] = df_ST['in_uptrend'][previous]
            
#             if df_ST['in_uptrend'][current] and df_ST['lowerband'][current]< df_ST['lowerband'][previous]:
#                 df_ST['lowerband'][current] = df_ST['lowerband'][previous]
            
#             if not df_ST['in_uptrend'][current] and df_ST['upperband'][current]>df_ST['upperband'][previous]:
#                 df_ST['upperband'][current] = df_ST['upperband'][previous]
        
    
#     return df_ST

# #****Calculating RSI******

# # def check_RSI(df_ST):
# #     np_closes = numpy.array(closes)
# #     last_close = df_ST['close'].tail(1)
# #     closes.append(float(last_close))
# #     if len(closes)> RSI_PERIOD:
# #         rsi = talib.RSI(np_closes, RSI_PERIOD)
# #         print(f'The Current RSI is {rsi}')
# #     else:
# #         print('still calculating....')


# def check_buy_sell_signals (df_ST):
#     global in_position
#     global order_buy_price
#     global order_sell_price
#     print(f'in postion {in_position}')
#     print (colored("Checking for buy and sell signals",'red'))
#     #Rsi_Calculator()
#     print(colored(df_ST.tail(10),'blue'))
#     last_row_index = len(df_ST.index) - 1
#     previous_row_index = last_row_index - 1
#     closed_order = exchange.fetchClosedOrders('ICP/USDT')
    
#     price = closed_order[-1]
#     last_order_price = price['price']
#    # if not df_ST['in_uptrend'][previous_row_index] and df_ST['in_uptrend'][last_row_index]  :
#     if Rsi_Calculator() < RSI_OVERSOLD :
#         print("Changed To Uptrend ! buy")
#         if not in_position:
#             #order= exchange.create_market_buy_order('ICP/USDT', 0.1)
#             order = 'this is a buy order'
#             print(order)
#             in_position = True
#             order_buy_price = current_price()
#             print(order_buy_price)
#         else :
#             print("We are already in position just wait Dude  !")

#     #if df_ST['in_uptrend'][previous_row_index] and not df_ST['in_uptrend'][last_row_index] :
#     if in_position and  Rsi_Calculator() > RSI_OVERBOUGHT or current_price() > order_buy_price+2 :
#         if current_price() > order_buy_price :
#             print("changed to downtrend ! Sell")
#             #order = exchange.create_market_sell_order('ICP/USDT', 0.1)
#             order_sell = 'The sell order is done with succes '
#             print(order_sell)
#             order_sell_price = current_price()
#             print (f'we bought the order at{order_buy_price} and we sell it for {order_sell_price} and we made {order_sell_price-order_buy_price} USDT')
#             file1 = open("deals.txt","a")
#             file1.write(str(f'we bought the order at{order_buy_price} and we sell it for {order_sell_price} and we made {order_sell_price-order_buy_price} USDT'))
#             file1.write("\n")
#             file1.close
#             in_position = False
#         elif in_position and current_price() < order_buy_price :
#             print("You are in Position But we keep looking for better price ! ")
#             file1 = open("deals.txt","a")
#             file1.write("You are in Position But we keep looking for better price ! ")
#             file1.write("\n")
#             file1.close
        
#         else: 
#             print ("You are not in postion Nothing to do !")

    
# def run_bot():
#     print(Fore.BLUE+f"Fetching new Bars for {datetime.datetime.now().isoformat()}......")
#     bars_ST = exchange.fetch_ohlcv('ICP/USDT',timeframe='1m', limit=100)
#     df_ST = pd.DataFrame(bars_ST[:-1], columns=['timestamp','open','high','low','close','volume'])
#     df_ST['timestamp'] = pd.to_datetime(df_ST['timestamp'],unit='ms')
#     #print(df_ST)
#     supertrend_data =  supertrend(df_ST)
#     check_buy_sell_signals(supertrend_data)
    
    
    
# schedule.every(5).seconds.do(run_bot)

# #? Check later if you gonna use it to display 
# #supertrend(df_ST) 

# while True:
#     schedule.run_pending()
#     time.sleep(1)








































# # # ** RSI n Order 
# # def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
# #     try:
# #         print("sending order")
# #         order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
# #         print(order)
# #     except Exception as e:
# #         print("an exception occured - {}".format(e))
# #         return False

# #     return True
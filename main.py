import bot as trader
import Market_Trend as MT
import multiprocessing as mp
import threading
import time
import schedule
import yoda


# ? Desactivate Those two lines to make test with just one trading Pair
# TRADE_SYMBOLE = 'ICP/USDT'
# Tr = 'BNB/USDT'
Pairs = ['BTC','LTC','BNB','MDX','CHZ','SUPER','EOS','LINK','TRX','VET','ATA','ASR','ALICE']
Tradable_Pairs = []
Currency = '/USDT'

# #* Testing The Rising Markets in The last 12 Hours 
# yoda.send_message(str(f'Dark is restarting  ....... !!! \U00002714')) 
# yoda.send_message(str(f'Trading in Risky Mode and TP is 2.7% \U00002747 \U00002747 \U00002747 \U00002747'))  
for pair in range(len(Pairs)):
    CURRENT_PAIR = Pairs[pair] + Currency
    Tradable_Pairs.append(CURRENT_PAIR)
    TREND = MT.Market_Trend(CURRENT_PAIR,'1h'x,100)
    print(TREND.tail(1))
    for current in range (len(TREND.index)-6, len(TREND.index)):
        previous = current - 1
        if TREND['in_uptrend'][current] == TREND['in_uptrend'][previous] == True :
            Is_UP = True
        else :
            Is_UP = False
    if not Is_UP:
        
        msg = f'The Current {CURRENT_PAIR} MARKET IS UP'
    print(f'***** This Pair is **** {Is_UP}')
print(f'The Tradable Pairs for today are {Tradable_Pairs}')
yoda.send_message(str(f'The Best Pairs for The Last 12 Hours are {Tradable_Pairs} !!!'))  
print('Start Trading.......') 
print("Number of processors: ", mp.cpu_count())
yoda.send_message(str(f'Yoda is Adjusting TP and Stop Loss \U00002728 ')) 
yoda.send_message(str(f'Yoda Resumed previous positions \U0001f300 \U0001f300 \U0001f300 !!!')) 
      
        
    


if len(Tradable_Pairs) > 0:
    def run_threaded(job_func):
        job_thread = threading.Thread(target=trader.Bot_trader(Tradable_Pairs[0],12))
        job_thread =  threading.Thread(target=trader.Bot_trader(Tradable_Pairs[1],12))
        job_thread = threading.Thread(target=trader.Bot_trader(Tradable_Pairs[2],12))
        job_thread = threading.Thread(target=trader.Bot_trader(Tradable_Pairs[3],12))
        job_thread = threading.Thread(target=trader.Bot_trader(Tradable_Pairs[4],12))
        job_thread = threading.Thread(target=trader.Bot_trader(Tradable_Pairs[5],12))
        job_thread = threading.Thread(target=trader.Bot_trader(Tradable_Pairs[6],12))
        job_thread = threading.Thread(target=trader.Bot_trader(Tradable_Pairs[7],12))
        job_thread = threading.Thread(target=trader.Bot_trader(Tradable_Pairs[8],12))
        job_thread = threading.Thread(target=trader.Bot_trader(Tradable_Pairs[9],12))
       

        
        job_thread.start()
    schedule.every(2).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[0],14))
    schedule.every(1).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[1],14))
    schedule.every(2).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[2],14))
    schedule.every(1).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[3],14))
    schedule.every(3).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[4],14))
    schedule.every(3).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[5],14))
    schedule.every(4).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[6],14))
    schedule.every(4).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[5],14))
    schedule.every(5).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[7],14))
    schedule.every(6).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[8],14))
    schedule.every(6).seconds.do(run_threaded, trader.Bot_trader(Tradable_Pairs[9],14))

else :
    print("Sorry ALL The markets are down for Daily Trading ")
    exit()

while 1:
    schedule.run_pending()
    time.sleep(1)




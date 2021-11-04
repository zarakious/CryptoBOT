# API  : 'Telegram API_KEY'
# CHAT ID  : Your Chat ID Here
#
#
import telegram
import constants
chat_id = constants.Chat_id
my_token = constants.API_KEY
msg = 'This is a simple text message for testing'

def send_message (msg,chat_id=chat_id,token=my_token):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id,text=msg)

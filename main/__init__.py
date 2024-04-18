#ChauhanMahesh/Vasusen/DroneBots/COL

from pyrogram import Client
from telethon import TelegramClient
# from decouple import config
import logging, time, sys, uvloop

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = 2992000
API_HASH = "235b12e862d71234ea222082052822fd"
BOT_TOKEN = "6633102102:AAEZLOFpQUfOHvNgBdAlJ7H52hnOXaUMpfY"
FORCESUB = int("-1001711957758")
ACCESS = int("-1001879806908")
ACCESS2 = int("-1001823465454")
MONGODB_URI = "mongodb+srv://thechauhanmahesh:XgbFpSEe3pM9P45z@cluster0.mkaomd0.mongodb.net"
AUTH_USERS = 1807573686
BOT_UN = "PremiumSRCB_DC2Bot"

"""
dc2 : 6710941011:AAFVG83NRSnaohlnYR_KCM1MtnWPnsDbiuY
m1 : 6633102102:AAEZLOFpQUfOHvNgBdAlJ7H52hnOXaUMpfY
m2 : 6727567600:AAHANjv_kposAf3R9B263O1IsfzWmeUs77Y
"""
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)    


try:
    Bot.start()
except Exception as e:
    print(e)
    sys.exit(1)

#ChauhanMahesh/Vasusen/DroneBots/COL

from pyrogram import Client
from telethon import TelegramClient
#from decouple import config
import logging, time, sys

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

"""
D: 6125089272:AAEDF254YhMbUK5hhl0yFbEQTqlhgA3W0jc

6077629818:AAFTBqay0B_4yD_LrwnfpfAU2fcXU5Vs2bU
"""
# variables
API_ID = 2992000
API_HASH = "235b12e862d71234ea222082052822fd"
BOT_TOKEN = "6125089272:AAEDF254YhMbUK5hhl0yFbEQTqlhgA3W0jc"
FORCESUB = ["Save_restricted_content_1", "Save_Restricted_Message"]
ACCESS = int("-1001768362393")
ACCESS2 = int("-1001823465454")
MONGODB_URI = "mongodb+srv://thechauhanmahesh:XgbFpSEe3pM9P45z@cluster0.mkaomd0.mongodb.net"
AUTH_USERS = 1807573686

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

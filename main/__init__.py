#ChauhanMahesh/Vasusen/DroneBots/COL

from pyrogram import Client
from telethon import TelegramClient
from decouple import config
import logging, time, sys

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

"""
ps2 : 5832484897:AAF9XsvYlzaMJWrS6hq14yaEu_RKjzT84-8
ps1 : 5926923294:AAE-f__dTNABjmN-4GfLzKQopGhLB5S9mp8
ps3 : 6379096336:AAHKVOvumm-ErIn1bRPsHK9P3wkjw4jS5ik
ps4 : 6401894192:AAFVDctSK9k3v3z7oTdtbweGLb5gmeUTxRw

p : 6077629818:AAFTBqay0B_4yD_LrwnfpfAU2fcXU5Vs2bU
"""

# variables
API_ID = 2992000
API_HASH = "235b12e862d71234ea222082052822fd"
BOT_TOKEN = "5832484897:AAF9XsvYlzaMJWrS6hq14yaEu_RKjzT84-8"
FORCESUB = int("-1001711957758")
ACCESS = int("-1001879806908")
ACCESS2 = int("-1001823465454")
MONGODB_URI = "mongodb+srv://Vasusen:darkmaahi@cluster0.o7uqb.mongodb.net/cluster0?retryWrites=true&w=majority"
AUTH_USERS = 5351121397
BOT_UN = "Premiumsrcb2_bot"

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

uploader_ubot = Client(
  "uploader_ubot",
  session_string="BQBJMj4ALoxz43Ny9hDpWMxhMEy4ZAZIgiyFqaYU4NnVQi3k5bHyTHdQpZNRE_HE_RcTvJl3dKjDP7sIwAFSRyCP7IOz6o84wHWQUxUZBbqIONKla2MuCiU63zdlt-BmMLTJPqoFRpUGI6zkdxdQzMIIlMhHHJ4Pn7LNvbdF4wos0oQ_f-H42ihQml5pP4vfdDA22xUuhZmnMyzIYcxY5OE4Wvp1OFaXu9Clw4vbbHotiCKWjq9irF7zB6uueWxMgis2HycrpOqCmlE_tIsEOiR2LQ4TgRy_PhrdGM3U9Ia09JrMuCccQy306J-eo16aB7WZKrEb7xBvDfZxos7iYWFLXQpjHwAAAABrvWK2AA", 
  api_hash=API_HASH, 
  api_id=API_ID, 
  max_concurrent_transmissions=5
) 

"""
try:
    uploader_ubot.start()
except BaseException:
    print("Userbot Error !")
"""

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

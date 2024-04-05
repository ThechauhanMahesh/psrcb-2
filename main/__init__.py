#ChauhanMahesh/Vasusen/DroneBots/COL

from pyrogram import Client
from telethon import TelegramClient
# from decouple import config
import logging, time, sys

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

"""
ps2 : 6890628049:AAG4LctwPDIIHYgG-RRDHD_BCPV67c36ut8
ps1 : 6900940299:AAEOPMETfJZrwwKvsx-5A9oFuv_nVs4jVq0
ps3 : 6757308177:AAEe364a_hMLcR4JFymFVXNYghEws7szoh8
ps4 : 6608701591:AAFERzaluRyq4dNHDQi5EdBNlLXffMeJdbQ
ps5 : 6669926453:AAEZc_j2UETA96mOgXTCWCmoi4RMfcdoycg
"""

# variables
API_ID = 2992000
API_HASH = "235b12e862d71234ea222082052822fd"
BOT_TOKEN = "6669926453:AAEZc_j2UETA96mOgXTCWCmoi4RMfcdoycg"
FORCESUB = int("-1001711957758")
ACCESS = int("-1001879806908")
ACCESS2 = int("-1001823465454")
MONGODB_URI = "mongodb+srv://thechauhanmahesh:XgbFpSEe3pM9P45z@cluster0.mkaomd0.mongodb.net"
AUTH_USERS = 1807573686

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

uploader_ubot = Client(
  "uploader_ubot",
  session_string="BQAtp4AAhtF1yIVdl0YOozgeVFGIo9_EFzMLLLYvOgJpyfyo0FNsUmNN41TG5IMbZt7vVIfHJnDYqJ1xzDKHi9SD2-wRmeHYIiBkpDP4ziJ2aVdPWuiX6aSyW5wCQdSiuhNgAlT6wTVsR8Fh9LwliU65W2Aic_1eFAvlpD-EgvGr7KWm67J6xrv0FGSH6ZHncV-OBaWMCK3iO2dvGgKef47e6a1KGulBsjjehh4xla2gKGTPLaWD06AqvvQ3q9pjwrevw7GiSkpCC0yFwD85M5Yr3wIkiNMXh6ndOe4bDTpSG4_se7nxKQP5TbxxfmjaqKqByuVWrzuD9cinns7HaxEgndswVQAAAABrvWK2AA", 
  api_hash=API_HASH, 
  api_id=API_ID, 
  max_concurrent_transmissions=5
) 


try:
    uploader_ubot.start()
except BaseException:
    print("Userbot Error !")

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH,
    sleep_threshold=300,
    workers=343
)    

try:
    Bot.start()
except Exception as e:
    print(e)
    sys.exit(1)

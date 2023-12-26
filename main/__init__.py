#ChauhanMahesh/Vasusen/DroneBots/COL

from pyrogram import Client
from telethon import TelegramClient
from decouple import config
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
BOT_TOKEN = "6608701591:AAFERzaluRyq4dNHDQi5EdBNlLXffMeJdbQ"
FORCESUB = int("-1001711957758")
ACCESS = int("-1001879806908")
ACCESS2 = int("-1001823465454")
MONGODB_URI = "mongodb+srv://Vasusen:darkmaahi@cluster0.o7uqb.mongodb.net/cluster0?retryWrites=true&w=majority"
AUTH_USERS = 5351121397
BOT_UN = "Premiumsrcb2_bot"

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

uploader_ubot = Client(
  "uploader_ubot",
  session_string="BQAtp4AAa0F7MognMniEO0Bx5QCO___MnxHTRnA2e6abBqFJ_MzKmMTrYOoV6R6LznK9d1ArPh6Py5KcHsJaIzXQVG0Kp0zAhSfbbBbbY1hnsbNVTGy6BY99d53We42MQFWyuXAuQxioshK--pej0-6jzdw6TfcUdwEWCeCNEOos7LMIgaOZUyyyAODRt-AOpJe_mv2sRwE9R1FcyfRzzKEb4po-ki1CXoEywdswE7C34l0WxCpyRGY-gNPRe3YapUQhG8D6bUB3Lvd6aa5U4rtue99ulYuxMC5QoR5x1Csi9FQy7d8iDUy61ahFKkS8GrtpNLprovQp9471_-Y6snrIlffZ0AAAAABrvWK2AA", 
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
    api_hash=API_HASH
)    

try:
    Bot.start()
except Exception as e:
    print(e)
    sys.exit(1)

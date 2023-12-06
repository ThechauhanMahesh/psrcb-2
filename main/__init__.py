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
BOT_TOKEN = "5926923294:AAE-f__dTNABjmN-4GfLzKQopGhLB5S9mp8"
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

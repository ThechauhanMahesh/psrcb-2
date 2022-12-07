#ChauhanMahesh/Vasusen/DroneBots/COL

from pyrogram import Client
from telethon import TelegramClient
from decouple import config
import logging, time, sys

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = 25391807
API_HASH = "c3aac9db5221dd2ca5aeb60ad8e0c712"
BOT_TOKEN = "5710340586:AAGbLqvTRmhWDVjiIHQboSIWr2NkE0aNbVw"
FORCESUB = int("-1001711957758")
ACCESS = int("-1001885911868")
MONGODB_URI = "mongodb+srv://Vasusen:darkmaahi@cluster0.o7uqb.mongodb.net/cluster0?retryWrites=true&w=majority"
AUTH_USERS = 5351121397

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

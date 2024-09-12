#ChauhanMahesh/Vasusen/DroneBots/COL

import os
from pyrogram import Client
from pyromod import listen
import logging, sys, pymongo

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

help_text = """Help:

**FOR PUBLIC CHANNEL:**
- Send me direct link of message. 

**FOR PRIVATE CHANNEL:**
- Login 
- Then send Link of message of any channel you've joined.

#FAQ 

- If bot says “Have you joined the channel?” Then just login again in bot and try.

- If bot says “Please don't spam links, wait until ongoing process is done.” then send /free command in bot and try after 10 minutes. 

- if bot says “Login credentials not found” the just login again

- If bot shows error containing “AUTH_KEY_DUPLICATED” in it then login again.

- if you batch is stuck then use /cancel 

#Note : Don't use the /free command unnecessarily.
"""

otp_text = """An OTP has been sent to your number. 

Please send the OTP with space, example: `1 2 3 4 5`."""


"""
ps2 : 6890628049:AAG4LctwPDIIHYgG-RRDHD_BCPV67c36ut8
ps1 : 6900940299:AAEOPMETfJZrwwKvsx-5A9oFuv_nVs4jVq0
ps3 : 6757308177:AAEe364a_hMLcR4JFymFVXNYghEws7szoh8
ps4 : 6608701591:AAFERzaluRyq4dNHDQi5EdBNlLXffMeJdbQ
ps5 : 6669926453:AAEZc_j2UETA96mOgXTCWCmoi4RMfcdoycg
ps6 : 7418708792:AAHPbkpibhfE4chJRUmacErpB1Z3zyBuJDY
ps7 : 7424086573:AAHdmAJyM8bS0Lqk2V2Y1e2SVbPFJnRlOOE
"""

"""
1 : 7058775123:AAHo7l0Q2GQmhFhe-syVNsTYzhiL0cqox9Y
2 : 7040936113:AAHAeQpQdU3M86kFfHMK0k6DYP5nwpDcTec
3 : 6765018152:AAGYr-Tjy6eiodbEy7mNbAkJx1JwZPtGGmM
4 : 6671807633:AAHIt90EbxXdH7BVwsMVeXJSdNr1bT_eATw
"""


# variables
API_ID = 2992000
API_HASH = "235b12e862d71234ea222082052822fd"
BOT_TOKEN = "6671807633:AAHIt90EbxXdH7BVwsMVeXJSdNr1bT_eATw"
FORCESUB = int("-1001711957758")
ACCESS = int("-1001879806908")
MONGODB_URI = "mongodb+srv://thechauhanmahesh:XgbFpSEe3pM9P45z@cluster0.mkaomd0.mongodb.net"
AUTH_USERS = 1807573686
SESSION_NAME = "PremiumSRCB"
PYRO_DIR = "pyro-sessions"

# list of telegram bot tokens
UPLOADING_CLIENTS = [
  "6757308177:AAEe364a_hMLcR4JFymFVXNYghEws7szoh8", 
  "6608701591:AAFERzaluRyq4dNHDQi5EdBNlLXffMeJdbQ", 
  "6669926453:AAEZc_j2UETA96mOgXTCWCmoi4RMfcdoycg", 
  "7418708792:AAHPbkpibhfE4chJRUmacErpB1Z3zyBuJDY",
  "7424086573:AAHdmAJyM8bS0Lqk2V2Y1e2SVbPFJnRlOOE"]

DUMP_CHANNEL = "-1002361531247"

client = pymongo.MongoClient(MONGODB_URI)
db = client[SESSION_NAME]
collection = db["users"]
process = {"process":{"process":False, "batch":False}}
collection.update_many({}, {"$set":process})
print("All users have been set free.")


class CustomBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = {}
        if not os.path.isdir(PYRO_DIR):
            os.makedirs(PYRO_DIR)

    def load_clients(self):
        for num, token in enumerate(UPLOADING_CLIENTS, start=1):
            try:
                print(f"[{num}/{len(UPLOADING_CLIENTS)}] adding client")
                client = Client(f"client_{num}", api_id=API_ID, api_hash=API_HASH, bot_token=token, no_updates=True, workdir=PYRO_DIR)
                client.start()
                self.clients[num] = {
                    "client": client, 
                    "process_count": 0,
                    "num": num,
                }
            except Exception as e: 
                print(f"[{num}/{len(UPLOADING_CLIENTS)}] error : {e}") 
        print("All clients loaded!")

    def get_client(self):
        try:
            sorted_clients = sorted(self.clients.values(), key=lambda x:x.get('process_count'))
            if sorted_clients:
                sorted_clients[0]['process_count'] += 1
                return sorted_clients[0]
        except: 
            print("No clients available to use")
            return 

    def release_client(self, num):
        if isinstance(num, dict):
            num = num.get('num')
        try:
            self.clients[num]['process_count'] -= 1
        except:
            print(f"error releasing client {num}")

    def start(self, **kwargs):
        super().start(**kwargs)
        self.username = self.get_me().username
        print(f"Bot started as {self.username}")

    def stop(self, **kwargs):
        super().stop(**kwargs)
        print("Stopping all clients")
        for client in self.clients.values():
            client['client'].stop()
        print("Bot stopped")

bot = CustomBot(
    "PyrogamBot",
    api_hash=API_HASH,
    api_id=API_ID,
    bot_token=BOT_TOKEN,
    workdir=PYRO_DIR,
    workers=343
    ) # pyrogram bot

bot.load_clients()

#ChauhanMahesh/Vasusen/DroneBots/COL

import asyncio
import os
from pyrogram import Client
from pyromod import listen
import logging, sys, pymongo

logging.basicConfig(
    format = "[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler("log.txt", "w"), logging.StreamHandler()],
    level=logging.ERROR
)

"""
Js :

API_ID= 23396174
API_HASH= "7a138e917e0d16e102d7bc74fa8828c0"

API_ID= 20261016
API_HASH= "23240f2a7b2e08a801e8a5b3d787fc9e"

API_ID = 27427306
API_HASH = "12a0c2a67e79cbf8284aa5e2cbd3ad04"

Jb:

API_ID = 28938535
API_HASH = "7b3be0a2d8c16bc23d340da4748b12ae"

API_ID = 10355467
API_HASH = "d86087c1892f818da03d68c3eaba765c" 

"""

"""
JS
1 : 7873589611:AAFC9co4DQALF4G1t1d1_AYCUMN6ICGyiro
2 : 7903237240:AAFT_XFw3Z8Z8xHc93si816V9eTrwZ6vUGQ
3 : 7730983772:AAEDch6rs1r24Ved-nt1Okf37LlqXE2rowU

JB 
1 : 7592623182:AAG8g-Ez5aniRSG0k_VPRkFzDwgiOcfEaf4
2 : 8178118562:AAEz3HhlJzWTLAKCMrG-JwEOP5ZmrYfqiPo
"""


# variables
API_ID = 28938535
API_HASH = "7b3be0a2d8c16bc23d340da4748b12ae"
BOT_TOKEN = "7592623182:AAG8g-Ez5aniRSG0k_VPRkFzDwgiOcfEaf4"
FORCESUB = int("-1001711957758")
ACCESS = int("-1001879806908")
MONGODB_URI = "mongodb+srv://thechauhanmahesh:XgbFpSEe3pM9P45z@cluster0.mkaomd0.mongodb.net"
AUTH_USERS = [1807573686, 1204927413]
SESSION_NAME = "PremiumSRCB"
PYRO_DIR = "pyro-sessions"
DL_DIR = "downloads"
batch_not_allowed = False

DUMP_CHANNEL = -1002651267079

SPLIT_SIZE = 2097152000 # 2 GB


# list of telegram bot tokens
UPLOADING_CLIENTS = []
if batch_not_allowed:
    UPLOADING_CLIENTS = [
        "8068044337:AAGan2FqDbYkWjhweuifBuCBcZga-fxxQK4",
        "7985855882:AAHq3A6CldHSSt-TZmXqWInqfl4uL6wHj0Q",
        "7382442840:AAGK9b7M14IbSQHXm7EzLYzOPwPqYngvppA"]
else:
    UPLOADING_CLIENTS = [
        "7424086573:AAHdmAJyM8bS0Lqk2V2Y1e2SVbPFJnRlOOE",
        "7418708792:AAHPbkpibhfE4chJRUmacErpB1Z3zyBuJDY",
        "7368658954:AAGQQDUbBil4h7WvChhS__0cTxRt7qzdPt0"]


client = pymongo.MongoClient(MONGODB_URI)
db = client[SESSION_NAME]
collection = db["users"]
process = {"process":{"process":False, "batch":False}}
collection.update_many({}, {"$set":process})
print("All users have been set free.")

class CustomUser(object):
    def __init__(self, user_id):
        self.id = user_id
        self.username = user_id

class CustomBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = {}
        # TELEGRAM DESKTOP (Default)
        if not self.api_id or not self.api_hash:
            self.api_id = 2040
            self.api_hash ="b18441a1ff607e10a989891a5462e627"
        self.system_version = "Windows 11"
        self.app_version = "5.12.3 x64"
        self.lang_code = "en"
        self.system_lang_code = "en-US"
        self.lang_pack = "tdesktop"
        if not os.path.isdir(PYRO_DIR):
            os.makedirs(PYRO_DIR)
        if not os.path.isdir(DL_DIR):
            os.makedirs(DL_DIR)

    def load_clients(self):
        if not os.path.isdir(PYRO_DIR):
            os.makedirs(PYRO_DIR)
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
            if sorted_clients := sorted(
                self.clients.values(), key=lambda x: x.get('process_count')
            ):
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

    async def start(self, **kwargs):
        await super().start(**kwargs)
        try:
            self.me = await self.get_me()
        except:
            await asyncio.sleep(5)
            if user:=collection.find_one({"session": self.session_string}):
                self.me = CustomUser(user["id"])
            else:
                self.me = CustomUser(int(BOT_TOKEN.split(":")[0]))
        self.username = self.me.username or self.me.id
        user_dir = os.path.join(DL_DIR, str(self.me.id))
        if not os.path.isdir(user_dir):
            os.makedirs(user_dir)
        print(f"Bot started as {self.username}")

    async def stop(self, **kwargs):
        await super().stop(**kwargs)
        if self.me.id == int(BOT_TOKEN.split(":")[0]):
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
    # workers=10
    ) # pyrogram bot

bot.load_clients()

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


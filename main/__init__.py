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
API_ID= 23396174
API_HASH= "7a138e917e0d16e102d7bc74fa8828c0"

API_ID=20261016
API_HASH=23240f2a7b2e08a801e8a5b3d787fc9e

"""

"""
1 : 7224876953:AAH0YHzG9td8qEsiGQEyrdsjwZnyPu176mQ
2 : 7903561520:AAEXbRWfYSTPnYe7fNNarMUIngGberFKjIo
3 : 6765018152:AAGYr-Tjy6eiodbEy7mNbAkJx1JwZPtGGmM
4 : 7588098571:AAGWIYs2e8rn6g7AT5w7GjBj99SJLUpcslc
"""


# variables
API_ID= 20261016
API_HASH= "23240f2a7b2e08a801e8a5b3d787fc9e"
BOT_TOKEN = "7903237240:AAFT_XFw3Z8Z8xHc93si816V9eTrwZ6vUGQ"
FORCESUB = int("-1001711957758")
ACCESS = int("-1001879806908")
MONGODB_URI = "mongodb+srv://thechauhanmahesh:XgbFpSEe3pM9P45z@cluster0.mkaomd0.mongodb.net"
AUTH_USERS = [1807573686, 1204927413]
SESSION_NAME = "PremiumSRCB"
PYRO_DIR = "pyro-sessions"
DL_DIR = "downloads"
ONGOING = 0

# list of telegram bot tokens
UPLOADING_CLIENTS = [
  "7382442840:AAELkZn7Ytl4v1H2v3xEnLZn_0d0iD8045E",
  "7985855882:AAEJ_iXQ9WnV2TjPGoul4nTfkzv8JFvX8yQ",
  "8068044337:AAGnVTzVBEsyqeZvT9As2AwRd48KUuvTYLc"]
  #"7833654484:AAGdrhuCGFyQJm07uY3AU96DJPuyi39CGEA"]

DUMP_CHANNEL = -1002892267641

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

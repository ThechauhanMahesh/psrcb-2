#ChauhanMahesh/Vasusen/DroneBots/COL

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

# variables
API_ID = 2992000
API_HASH = "235b12e862d71234ea222082052822fd"
BOT_TOKEN = "6669926453:AAEZc_j2UETA96mOgXTCWCmoi4RMfcdoycg"
FORCESUB = int("-1001711957758")
ACCESS = int("-1001879806908")
MONGODB_URI = "mongodb+srv://thechauhanmahesh:XgbFpSEe3pM9P45z@cluster0.mkaomd0.mongodb.net"
AUTH_USERS = 1807573686
SESSION_NAME = "PremiumSRCB"

client = pymongo.MongoClient(MONGODB_URI)
db = client[SESSION_NAME] 
collection = db["users"]  
process = {"process":{"process":False, "batch":False}}
collection.update_many({}, {"$set":process})
print("All users have been set free.")

bot = Client(
    "PyrogamBot", 
    api_hash=API_HASH, 
    api_id=API_ID, 
    bot_token=BOT_TOKEN,
    workers=343
    ) # pyrogram bot

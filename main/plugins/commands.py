#Github.com/Vasusen-code

import os, asyncio
from .. import bot as Drone, API_ID, API_HASH, help_text as ht, otp_text, AUTH_USERS

from pyrogram import Client, filters, types
from pyrogram.errors import SessionPasswordNeeded, FloodWait, PhoneCodeInvalid, PhoneCodeExpired 

from main.plugins.helpers import login, logout
from main.Database.database import db

APIID = [API_ID, 29841594]
APIHASH = [API_HASH, "1674d13f3308faa1479b445cdbaaad2b"]

@Drone.on_message(filters=filters.private & filters.incoming, group=1)
async def incomming(client, message: types.Message):
    user_id = message.from_user.id
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
        tag = f'[{message.from_user.first_name}](t.me/@id{user_id})'
        await Drone.send_message(int(AUTH_USERS), f'Activate the plan of {tag}\nUserID: {user_id}') 
        await message.reply("Purchase premium from @SubscriptionForBot.")
    else:
        if (await db.get_data(user_id))["dos"] == None:
            tag = f'[{message.from_user.first_name}](t.me/@id{user_id})'
            await Drone.send_message(int(AUTH_USERS), f'Activate the plan of {tag}\nUserID: {user_id}') 

# @Drone.on(events.NewMessage(incoming=True, pattern="^/setchat (.*)" ))
# async def update_chat(event):
#     c = event.pattern_match.group(1)
#     await db.update_chat(event.sender_id, int(c))
#     await event.reply(f"Done.")

# @Drone.on(events.NewMessage(incoming=True, pattern="/remchat" ))
# async def rem_chat(event):
#     await db.rem_chat(event.sender_id, event.sender_id)
#     await event.reply(f"Done.")

@Drone.on_message(filters=filters.command('start') & filters.incoming)
async def start(_, message: types.Message):
    await message.reply("Send me **link** of any **public** channel message to clone it here 🔗, For **private** channel message, First **/login** then send any **message link** from your chat ✅.\n\n**SUPPORT:** @TeamDrone\n**DEV:** @MaheshChauhan") 

@Drone.on_message(filters=filters.command('login') & filters.incoming)
async def login(_, message: types.Message):
    number, otp, code = 0, 0, 0
    session, passcode, ai, ah= None, None, None, None
    user_id = message.from_user.id

    contact = await Drone.ask(user_id, "Send me your contact number with country code(eg +1 or +91) to login.", filters=filters.text)
    number = ' '.join(str(contact.text))

    code_alert = await message.reply("Sending code...")

    ai = APIID[0]
    ah = APIHASH[0]
    client = Client(f"{user_id}_account", api_id=ai, api_hash=ah, in_memory=True)
    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    try:
        code = await client.send_code(number)
        await asyncio.sleep(1)
    except FloodWait:
        await client.disconnect()
        client = Client("my_account", api_id=APIID[-1], api_hash=APIHASH[-1])
        ai = APIID[-1]
        ah = APIHASH[-1]
        try:
            await client.connect()
        except ConnectionError:
            await client.disconnect()
            await client.connect()
        try:
            code = await client.send_code(number)
            await asyncio.sleep(1)
        except FloodWait as e:
            await code_alert.edit(f"Can't send code, you have Floodwait of {e.x} Seconds.")
            return
        except Exception as e:
            print(e)
            await code_alert.edit(f"**Error**: {str(e)}")
            return
        await code_alert.delete()

@Drone.on_message(filters=filters.command('logout') & filters.incoming)
async def logout(_, message: types.Message):
    edit = await message.reply("Trying to logout.")
    await logout(message.from_user.id)
    await edit.edit('✅ successfully Logged out.')

@Drone.on_message(filters=filters.command('logout') & filters.incoming)
async def help(_, message: types.Message):
    await message.reply(ht)

@Drone.on_message(filters=filters.command('setthumb') & filters.incoming)
async def setthumb(client, message: types.Message):   
    user_id = message.from_user.id
    image = await Drone.ask(user_id, "Send me any image for thumbnail.", filters=filters.photo)              
    edit = await message.reply("Trying to download..")
    path = await client.download_media(image)
    if os.path.exists(f'{user_id}.jpg'):
        os.remove(f'{user_id}.jpg')
    os.rename(path, f'./{user_id}.jpg')
    await edit.edit("✅ Temporary thumbnail saved!")

@Drone.on_message(filters=filters.command('remthumb') & filters.incoming)
async def remthumb(_, message: types.Message):             
    edit = await message.reply('Trying.')
    try:
        os.remove(f'{message.from_user.id}.jpg')
        await edit.edit('✅ Removed!')
    except Exception:
        await edit.edit("No thumbnail was saved.")     

    
    
    
    
    

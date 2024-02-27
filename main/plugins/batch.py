#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
Plugin for both public & private channels!
"""

import time, os, asyncio

from .. import bot as Drone, Bot, FORCESUB as fs, AUTH_USERS  as AUTH
from main.plugins.pyroplug import get_bulk_msg
from main.plugins.helpers import get_link, screenshot, force_sub, set_subscription, check_subscription
from main.Database.database import db

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

from ethon.pyfunc import video_metadata

errorC = """Error: Couldn't start client by Login credentials, Please logout and login again."""

conversation = []

@Drone.on(events.NewMessage(incoming=True, pattern='/cancel'))
async def cancel(event):
    async with event.client.conversation(event.sender_id, exclusive=False) as conv:
        await conv.cancel_all()
    if not (await db.get_process(event.sender_id))["batch"]:
        return await event.reply("No batch active, all previous conversations are cancelled.")
    await db.rem_process(event.sender_id)
    async with event.client.conversation(event.sender_id, exclusive=False) as conv:
        await conv.cancel_all()
    await event.reply("✅ Done.")

@Drone.on(events.NewMessage(incoming=True, pattern='/myplan'))
async def check_plan(event):
    data = await db.get_data(event.sender_id)
    await event.reply(f'**DATE OF SUBSCRIPTION:** {data["dos"]}\n**DATE OF EXPIRY:** {data["doe"]}\n**PLAN:** {data["plan"]}')
    return

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/ss'))
async def ss(event):
    edit = await event.reply("Processing...")
    msg = await event.get_reply_message()
    data = str(msg.text).split(" ")
    date = data[1]
    if date == "None":
        date = False
    await set_subscription(int(data[0]), date, int(data[2]), data[3])
    x = await db.get_data(int(data[0]))
    await edit.edit(f'{x}')
    await event.client.send_message(int(data[0]), "Your plan is active now, send /myplan to check.")
    return 

@Drone.on(events.NewMessage(incoming=True, pattern='/caption'))
async def _caption(event):
    if not (await db.get_data(event.sender_id))["plan"] == "pro":
        await event.reply("⚠️ Purchase pro plan.")
    await event.reply("Choose an action", buttons=[[Button.inline("OFF", data="off")],
                                                   [Button.inline("ADD", data="add")],
                                                   [Button.inline("DELETE", data="delete")],
                                                   [Button.inline("REPLACE", data="replace")]])

@Drone.on(events.callbackquery.CallbackQuery(data="add"))
async def _add(event):
    await event.delete()
    async with Drone.conversation(event.chat_id, exclusive=False) as conv: 
        await conv.send_message("Send the text you want to add in captions.")
        try:
            x = await conv.get_response()
        except:
            await conv.send_message("Cannot wait longer for your response.")
        await db.add_caption(event.sender_id, x.text)
        await conv.send_message("Done ✅")
        
@Drone.on(events.callbackquery.CallbackQuery(data="delete"))
async def delete(event):
    await event.delete()
    async with Drone.conversation(event.chat_id, exclusive=False) as conv: 
        await conv.send_message("Send the text you want to delete in captions.")
        try:
            x = await conv.get_response()
        except:
            await conv.send_message("Cannot wait longer for your response.")
        await db.delete_caption(event.sender_id, x.text)
        await conv.send_message("Done ✅")
        
@Drone.on(events.callbackquery.CallbackQuery(data="off"))
async def off(event):
    await event.delete()
    await db.disable_caption(event.sender_id)
    await event.client.send_message(event.sender_id, "No changes will be made in captions ✅")
    
@Drone.on(events.callbackquery.CallbackQuery(data="replace"))
async def replace(event):
    await event.delete()
    async with Drone.conversation(event.chat_id, exclusive=False) as conv: 
        await conv.send_message("Send the text you want to replace in captions.")
        try:
            text1 = await conv.get_response()
        except:
            await conv.send_message("Cannot wait longer for your response.")
        await conv.send_message("Send the text you want to replace by in captions.")
        try:
            text2 = await conv.get_response()
        except:
            await conv.send_message("Cannot wait longer for your response.")
        await db.replace_caption(event.sender_id, {"d":text1.text, "a":text2.text})
        await conv.send_message("Done ✅")
        
@Drone.on(events.NewMessage(incoming=True, pattern='/batch'))
async def _batch(event):
    if not event.is_private:
        return
    await check_subscription(event.sender_id)
    if (await db.get_data(event.sender_id))["plan"] == "basic":
        await event.reply("⚠️ Buy Monthly subscription or Pro subscription.")
        return
    pr = (await db.get_process(event.sender_id))["process"]
    if pr:
        return await event.reply("⚠️ You've already started one process, wait for it to complete!")
    async with Drone.conversation(event.chat_id, exclusive=False) as conv: 
        if pr != True:
            await conv.send_message("Send me the message link you want to start saving from, as a reply to this message.", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("⚠️ No link found.")
                    return await conv.cancel_all()
            except Exception as e:
                print(e)
                await conv.send_message("Cannot wait more longer for your response!")
                return await conv.cancel_all()
            await conv.send_message("Send me the number of files/range you want to save from the given message, as a reply to this message.", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                await conv.send_message("Cannot wait more longer for your response!")
                return await conv.cancel_all()
            try:
                value = int(_range.text)
                if value > 30:
                    if not (await db.get_data(event.sender_id))["plan"] == "pro":
                        await conv.send_message("⚠️ You can only get upto 30 files in a single batch.")
                        return await conv.cancel_all()
                    elif value > 100:
                        await conv.send_message("⚠️ You can only get upto 100 files in a single batch.")
                        return await conv.cancel_all()
            except ValueError:
                await conv.send_message("Range must be an integer!")
                return await conv.cancel_all()
            i, h, s = await db.get_credentials(event.chat.id)
            chat = await db.get_chat(event.chat.id)
            if chat == None:
                chat = event.sender_id
            userbot = None
            if i and h and s is not None:
                userbot = Client("saverestricted", session_string=s, api_hash=h, api_id=int(i))     
            else:
                await conv.send_message("⚠️ Your login credentials not found.")
                return await conv.cancel_all()
            await db.update_process(event.sender_id, batch=True)
            await run_batch(userbot, Bot, event.sender_id, chat, _link, value) 
            await conv.cancel_all()
            await db.rem_process(event.sender_id)
            
async def run_batch(userbot, client, sender, chat, link, _range):
    for i in range(_range):
        if i < 50:
            timer = 10
        elif i > 25 and i < 50:
            timer = 15
        elif i > 50 and i < 100:
            timer = 20
        elif i > 100:
            timer = 25
        if not 't.me/c/' in link and not 't.me/b/' in link:
            timer = 5
        if (await db.get_data(sender))["plan"] == "pro":
            if not 't.me/c/' in link and not 't.me/b/' in link:
                timer = 3
            else:
                timer = 2
                if i > 25 and i < 50:
                    timer = 5
                elif i > 50 and i < 100:
                    timer = 8
                elif i > 100:
                    timer = 10
        try: 
            if not (await db.get_process(sender))["process"]:
                await client.send_message(sender, "✅ Batch completed.")
                break
        except Exception as e:
            print(e)
            await client.send_message(sender, "✅ Batch completed.")
            break
        try: 
            await userbot.start()
        except Exception as e:
            print(e)
            await client.send_message(sender, f'{errorC}\n\n**Error:** {str(e)}')
            break
        try:
            await get_bulk_msg(userbot, client, sender, chat, link, i) 
        except FloodWait as fw:
            if int(fw.x) > 299:
                await client.send_message(sender, "❌ Cancelling batch since you have floodwait more than 5 minutes.")
                break
            await asyncio.sleep(fw.x + 5)
            await get_bulk_msg(userbot, client, sender, chat, link, i)
        await userbot.stop()
        protection = await client.send_message(chat, f"⚠️ Sleeping for `{timer}` seconds to avoid Floodwaits and Protect account!")
        await asyncio.sleep(timer)
        await protection.delete()
            

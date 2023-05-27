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

@Drone.on(events.NewMessage(incoming=True, pattern='/cancel'))
async def cancel(event):
    if not (await db.get_process(event.sender_id))["batch"]:
        return await event.reply("No batch active.")
    await db.rem_process(event.sender_id)
    await event.reply("Done.")

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

@Drone.on(events.NewMessage(incoming=True, pattern='/batch'))
async def _batch(event):
    if not event.is_private:
        return
    await check_subscription(event.sender_id)
    if (await db.get_data(event.sender_id))["plan"] == "basic":
        await event.reply("Buy Monthly subscription or Pro subscription.")
        return
    pr = (await db.get_process(event.sender_id))["process"]
    if pr:
        return await event.reply("You've already started one process, wait for it to complete!")
    async with Drone.conversation(event.chat_id) as conv: 
        if pr != True:
            await conv.send_message("Send me the message link you want to start saving from, as a reply to this message.", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("No link found.")
                    return conv.cancel()
            except Exception as e:
                print(e)
                await conv.send_message("Cannot wait more longer for your response!")
                return conv.cancel()
            await conv.send_message("Send me the number of files/range you want to save from the given message, as a reply to this message.", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                await conv.send_message("Cannot wait more longer for your response!")
                return conv.cancel()
            try:
                value = int(_range.text)
                if value > 20:
                    if not (await db.get_data(sender))["plan"] == "pro":
                        return await conv.send_message("You can only get upto 20 files in a single batch.")
                    elif value > 100:
                        return await conv.send_message("You can only get upto 100 files in a single batch.")
            except ValueError:
                return await conv.send_message("Range must be an integer!")
            i, h, s = await db.get_credentials(event.chat.id)
            chat = await db.get_chat(event.chat.id)
            if chat == None:
                chat = event.sender_id
            userbot = None
            if i and h and s is not None:
                userbot = Client("saverestricted", session_string=s, api_hash=h, api_id=int(i))     
            else:
                await conv.send_message("Your login credentials not found.")
                return conv.cancel()
            await db.update_process(event.sender_id, batch=True)
            await run_batch(userbot, Bot, event.sender_id, chat, _link, value) 
            conv.cancel()
            await db.rem_process(event.sender_id)
            
async def run_batch(userbot, client, sender, chat, link, _range):
    for i in range(_range):
        if i < 50:
            timer = 20
        elif i > 50 and i < 100:
            timer = 30
        elif i > 50 and i < 100:
            timer = 30
        elif i > 100:
            timer = 30
        if not 't.me/c/' in link and not 't.me/b/' in link:
            timer = 5
        if (await db.get_data(sender))["plan"] == "pro":
            if not 't.me/c/' in link and not 't.me/b/' in link:
                timer = 2
            else:
                timer = 2
        try: 
            if not (await db.get_process(sender))["process"]:
                await client.send_message(sender, "Batch completed.")
                break
        except Exception as e:
            print(e)
            await client.send_message(sender, "Batch completed.")
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
                await client.send_message(sender, "Cancelling batch since you have floodwait more than 5 minutes.")
                break
            await asyncio.sleep(fw.x + 5)
            await get_bulk_msg(userbot, client, sender, chat, link, i)
        await userbot.stop()
        protection = await client.send_message(chat, f"Sleeping for `{timer}` seconds to avoid Floodwaits and Protect account!")
        await asyncio.sleep(timer)
        await protection.delete()
            

#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
Plugin for both public & private channels!
"""

import time, os, asyncio

from .. import bot as Drone, MONGODB_URI, Bot, FORCESUB as fs, AUTH_USERS  as AUTH
from main.plugins.pyroplug import check, get_bulk_msg
from main.plugins.helpers import get_link, screenshot, force_sub
from main.Database.database import Database

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

from ethon.pyfunc import video_metadata

ft = f"To use this bot you've to join @{fs}."

batch = []
pros = []
monthly = []

async def get_pvt_content(event, chat, id):
    msg = await userbot.get_messages(chat, ids=id)
    await event.client.send_message(event.chat_id, msg) 
    
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/pros'))
async def pro(event):
    edit = await event.reply("Processing...")
    msg = await event.get_reply_message()
    pros.clear()
    for id in str(msg.text).split(" "):
        pros.append(id)
    await edit.edit(f"{pros}")

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/monthly'))
async def mo(event):
    edit = await event.reply("Processing...")
    msg = await event.get_reply_message()
    monthly.clear()
    for id in str(msg.text).split(" "):
        monthly.append(id)
    await edit.edit(f"{monthly}")

@Drone.on(events.NewMessage(incoming=True, pattern='/batch'))
async def _batch(event):
    if not event.is_private:
        return
    # wtf is the use of fsub here if the command is meant for the owner? 
    # well am too lazy to clean 
    if f'{event.sender_id}' not in monthly:
        if f'{event.sender_id}' not in pros:
            await event.reply("Buy Monthly subscription or Pro subscription.")
            return
    s = await force_sub(event.sender_id) 
    if s == True:
        await event.reply("You are not subscribed to premium bot, contact @ChauhanMahesh_BOT to buy.")
        return 
    if f'{event.sender_id}' in batch:
        return await event.reply("You've already started one batch, wait for it to complete!")
    async with Drone.conversation(event.chat_id) as conv: 
        if s != True:
            await conv.send_message("Send me the message link you want to start saving from, as a reply to this message.", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("No link found.")
            except Exception as e:
                print(e)
                return await conv.send_message("Cannot wait more longer for your response!")
            await conv.send_message("Send me the number of files/range you want to save from the given message, as a reply to this message.", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                return await conv.send_message("Cannot wait more longer for your response!")
            try:
                value = int(_range.text)
                if value > 10:
                    if f'{event.sender_id}' not in pros:
                        return await conv.send_message("You can only get upto 10 files in a single batch.")
                    elif value > 50:
                        return await conv.send_message("You can only get upto 50 files in a single batch.")
            except ValueError:
                return await conv.send_message("Range must be an integer!")
            db = Database(MONGODB_URI, 'saverestricted')
            i, h, s = await db.get_credentials(event.chat.id)
            userbot = None
            if i and h and s is not None:
                userbot = Client(session_name=s, api_hash=h, api_id=int(i))     
            else:
                ind = batch.index(f'{int(event.sender_id)}')
                batch.pop(int(ind))
                return await edit.edit("Your login credentials not found.")
            batch.append(f'{event.sender_id}')
            await run_batch(userbot, Bot, event.sender_id, _link, value) 
            conv.cancel()
            batch.pop(int(batch.index(f'{event.sender_id}')))
                  
async def run_batch(userbot, client, sender, link, _range):
    for i in range(_range):
        timer = 60
        if not 't.me/c/' in link:
            timer = 10
        try: 
            await userbot.start()
        except Exception as e:
            print(e)
            await client.send_message(sender, f'{errorC}\n\n**Error:** {str(e)}')
            break
        try:
            await get_bulk_msg(userbot, client, sender, link, i) 
        except FloodWait as fw:
            if int(fw.x) > 299:
                await client.send_message(sender, "Cancelling batch since you have floodwait more than 5 minutes.")
                break
            await asyncio.sleep(fw.x + 5)
            await get_bulk_msg(userbot, client, sender, link, i)
        await userbot.stop()
        protection = await client.send_message(sender, f"Sleeping for `{timer}` seconds to avoid Floodwaits and Protect account!")
        await asyncio.sleep(timer)
        await protection.delete()
            

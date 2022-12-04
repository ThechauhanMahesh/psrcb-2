# Github.com/Vasusen-code

from .. import bot as Drone
from .. import MONGODB_URI, Bot
from .. import FORCESUB as fs

from main.plugins.helpers import get_link, join, set_timer, check_timer, screenshot
from main.plugins.progress import progress_for_pyrogram
from main.Database.database import Database
from main.plugins.pyroplug import get_msg

from pyrogram.errors import FloodWait, BadRequest
from pyrogram import Client, filters, idle
from ethon.pyfunc import video_metadata
from ethon.telefunc import force_sub
from telethon import events

import re, time, asyncio
from decouple import config

ft = f"To use this bot you've to join @{fs}."

process=[]
timer=[]

errorC = """Error: Couldn't start client by Login credentials. Check these:

- is your API details entered right? 
- Did you send "Pyrogram" string session? 
- Do not send string in bold, italic or any other fonts."""

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    try:
        link = get_link(event.text)
        if not link:
            return
    except TypeError:
        return
    s = await force_sub(event.client, fs, event.sender_id, ft)
    if s == True:
        await event.reply("You are not subscribed to premium bot, contact @ChauhanMahesh_BOT to buy.")
        return
    edit = await event.reply("Processing!")
    if 't.me/+' in link:
        x, t = check_timer(event.sender_id, process, timer, 10) 
        if x == False:
            return await edit.edit(t)
        q = await join(userbot, link)
        await edit.edit(q)
        await set_timer(Drone, event.sender_id, process, timer, 10) 
        return 
    if 't.me' in link and not 't.me/c/' in link:
        x, t = check_timer(event.sender_id, process, timer, 10) 
        if x == False:
            return await edit.edit(t)
        await get_msg(None, Bot, Drone, event.sender_id, edit.id, link, 0)
        await set_timer(Drone, event.sender_id, process, timer, 10) 
    if 't.me/c/' in link:
        x, t = check_timer(event.sender_id, process, timer, 60) 
        if x == False:
            return await edit.edit(t)
        userbot = ""
        db = Database(MONGODB_URI, 'saverestricted')
        i, h, s = await db.get_credentials(event.chat.id)
        if i and h and s is not None:
            try:
                userbot = Client(session_name=s, api_hash=h, api_id=int(i))      
                await userbot.start()
            except ValueError:
                return await edit.edit("**INVALID API ID:** Logout and Login back with correct API ID.")
            except Exception as e:
                print(e)
                return await edit.edit(errorC)
        else:
            return await edit.edit("Your login credentials not found.")
        await get_msg(userbot, Bot, Drone,event.sender_id, edit.id, link, 0)
        await set_timer(Drone, event.sender_id, process, timer, 60) 

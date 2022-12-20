# Github.com/Vasusen-code

from .. import bot as Drone
from .. import MONGODB_URI, Bot, AUTH_USERS 
from .. import FORCESUB as fs

from main.plugins.helpers import get_link, join, set_timer, check_timer, screenshot, force_sub
from main.plugins.progress import progress_for_pyrogram
from main.Database.database import Database
from main.plugins.pyroplug import get_msg

from pyrogram.errors import FloodWait, BadRequest
from pyrogram import Client, filters, idle
from ethon.pyfunc import video_metadata
from telethon import events

import re, time, asyncio
from decouple import config

ft = f"To use this bot you've to join @{fs}."

process=[]
timer=[]
user = []

connection = []

errorC = """Error: Couldn't start client by Login credentials, Please logout and login again."""

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH_USERS, pattern="^/free (.*)"))
async def free(event):
    id = event.pattern_match.group(1)
    ind = user.index(f'{int(id)}')
    return user.pop(int(ind))

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    try:
        link = get_link(event.text)
        if not link:
            return
    except TypeError:
        return
    s = await force_sub(event.sender_id)
    if s == True:
        await event.reply("You are not subscribed to premium bot, contact @ChauhanMahesh_BOT to buy.")
        return
    edit = await event.reply("Processing!")
    if f'{int(event.sender_id)}' in user:
        return await edit.edit("Please don't spam links, wait until ongoing process is done.")
    user.append(f'{int(event.sender_id)}')
    if 't.me/+' in link:
        x, t = check_timer(event.sender_id, process, timer, 10) 
        if x == False:
            await edit.edit(t)
            ind = user.index(f'{int(event.sender_id)}')
            return user.pop(int(ind))
        q = await join(userbot, link)
        await edit.edit(q)
        await set_timer(Drone, event.sender_id, process, timer, 10) 
        ind = user.index(f'{int(event.sender_id)}')
        user.pop(int(ind))
        return 
    if 't.me' in link and not 't.me/c/' in link:
        x, t = check_timer(event.sender_id, process, timer, 10) 
        if x == False:
            await edit.edit(t)
            ind = user.index(f'{int(event.sender_id)}')
            return user.pop(int(ind))
        try:
            await get_msg(None, Bot, Drone, event.sender_id, edit.id, link, 0)
        except Exception as e:
            print(e)
            pass
        await set_timer(Drone, event.sender_id, process, timer, 10) 
        ind = user.index(f'{int(event.sender_id)}')
        user.pop(int(ind))
        return
    if 't.me/c/' in link:
        x, t = check_timer(event.sender_id, process, timer, 60) 
        if x == False:
            ind = user.index(f'{int(event.sender_id)}')
            user.pop(int(ind))
            return await edit.edit(t)
        userbot = ""
        db = Database(MONGODB_URI, 'saverestricted')
        i, h, s = await db.get_credentials(event.chat.id)
        if i and h and s is not None:
            try:
                userbot = Client(session_name=s, api_hash=h, api_id=int(i))     
                await userbot.start()
            except Exception as e:
                print(e)
                ind = user.index(f'{int(event.sender_id)}')
                user.pop(int(ind))
                await edit.edit(f'{errorC}\n\n**Error:** {str(e)}')
                return
        else:
            ind = user.index(f'{int(event.sender_id)}')
            user.pop(int(ind))
            return await edit.edit("Your login credentials not found.")
        try: 
            await get_msg(userbot, Bot, Drone,event.sender_id, edit.id, link, 0)
        except Exception as e:
            print(e)
            pass
        await set_timer(Drone, event.sender_id, process, timer, 60) 
        ind = user.index(f'{int(event.sender_id)}')
        user.pop(int(ind))

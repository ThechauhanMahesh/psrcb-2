# Github.com/Vasusen-code

from .. import bot as Drone
from .. import Bot, AUTH_USERS 

from main.plugins.helpers import get_link, check_subscription
from main.Database.database import db
from main.plugins.pyroplug import get_msg

from pyrogram import Client
from telethon import events

import asyncio
# from decouple import config

message = "Send me the message link you want to start saving from, as a reply to this message."
     
errorC = """Error: Couldn't start client by Login credentials, Please logout and login again."""

@Drone.on(events.NewMessage(incoming=True, pattern='/free'))
async def free(event):
    if not (await db.get_process(event.sender_id))["process"]:
        return
    if (await db.get_process(event.sender_id))["batch"]:
        return await event.reply("Use /cancel to stop batch.")
    await event.reply("Done, try after 10 minutes.")
    await asyncio.sleep(600)
    return await db.rem_process(int(event.sender_id))
   
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH_USERS, pattern="^/afree (.*)"))
async def afree(event):
    id = event.pattern_match.group(1)
    await db.rem_process(int(id))

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.text == message:
            return
    try:
        link = get_link(event.text)
        if not link:
            return
    except TypeError:
        return
    await check_subscription(event.sender_id)
    s = await db.get_data(event.sender_id)
    if s["dos"] == None:
        await event.reply("⚠️ You are not subscribed to premium bot, pay in @SubscriptionForBot to buy.")
        return
    edit = await event.reply("Processing!")
    if (await db.get_process(event.sender_id))["process"] == True:
        return await edit.edit("❌ Please don't spam links, wait until ongoing process is done.")
    timer = 10
    if (await db.get_data(event.sender_id))["plan"] == "pro":
        timer = 2
    to = await db.get_chat(event.chat.id)
    if to == None:
        to = event.sender_id
    if 't.me/+' in link:
        return await edit.edit("Join yourself manually.")
    if 't.me' in link:
        userbot = ""
        i, h, s = await db.get_credentials(event.chat.id)
        if i and h and s is not None:
            try:
                userbot = Client("saverestricted", session_string=s, api_hash=h, api_id=int(i))     
                await userbot.start()
            except Exception as e:
                print(e)
                return await edit.edit(str(e))
        else:
            return await edit.edit("⚠️ Your login credentials not found.")
        await db.update_process(event.sender_id)
        try: 
            await get_msg(userbot, Bot, event.sender_id, to, edit, link, i=0)
        except Exception as e:
            print(e)
            pass
        await userbot.stop()
        # add waiting period limit here of timer seconds

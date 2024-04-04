# Github.com/Vasusen-code

from .. import bot as Drone
from .. import Bot, AUTH_USERS 
from .. import FORCESUB as fs

from main.plugins.helpers import get_link, join, set_timer, screenshot, check_subscription, force_sub
from main.plugins.progress import progress_for_pyrogram
from main.Database.database import db
from main.plugins.pyroplug import get_msg

from pyrogram.errors import FloodWait, BadRequest
from pyrogram import Client, filters, idle
from ethon.pyfunc import video_metadata
from telethon import events, Button

import re, time, asyncio
# from decouple import config

process = 0

message = "Send me the message link you want to start saving from, as a reply to this message."
     
errorC = """Error: Couldn't start client by Login credentials, Please logout and login again."""

@Drone.on(events.NewMessage(incoming=True, pattern='/free'))
async def free(event):
    if not (await db.get_process(event.sender_id))["process"]:
        return
    if (await db.get_process(event.sender_id))["batch"]:
        return await event.reply("Use /cancel to stop batch.")
    await event.reply("Done, try after 60 minutes.")
    await asyncio.sleep(3600)
    return await db.rem_process(int(event.sender_id))
   
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH_USERS, pattern="^/afree (.*)"))
async def afree(event):
    id = event.pattern_match.group(1)
    await db.rem_process(int(id))

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    global process
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
    if not process < 26:
        return await event.reply("⚠️ Bot is overloaded with 25/25 proccesses, please wait or buy premium from @DroneBots")
    emoji = await event.reply("🔗")
    f = await force_sub(event.sender_id)
    if f:
        await emoji.delete()
        return await event.reply("⚠️ To use this bot you must **join** all below 3 channels", buttons=[[Button.url("JOIN 1", url="t.me/save_restricted_message")],
                                                                                                      [Button.url("JOIN 2", url="t.me/save_restricted_content_1")],
                                                                                                      [Button.url("JOIN 3", url="t.me/useful_premium_bots")]])
    count = await db.get_trial_count(event.sender_id)
    if count == 50:
        await emoji.delete()
        await event.reply("⚠️You have completed your trial of 50 links, please proceed to buy a paid plan from @DroneBOTs")
        n = await db.check_number(event.sender_id)
        if n:
            await db.black_list_number(event.sender_id)
        return
    n = await db.check_number(event.sender_id)
    if not n:
        await emoji.delete()
        return await event.reply("⚠️ Trials on this number is already over, buy premium subscription from @DroneBOTs")
    await emoji.delete()
    edit = await event.reply("Processing!")
    if (await db.get_process(event.sender_id))["process"] == True:
        return await edit.edit("❌ Please don't spam links, wait until ongoing process is done or buy premium subscription from @DroneBots.")
    pt = 600
    ut = 180
    to = await db.get_chat(event.chat.id)
    if to == None:
        to = event.sender_id
    if 't.me/+' in link:
        return await edit.edit("JOIN yourself manually.")
    if 't.me/c/' in link or 't.me/b/' in link:
        userbot = ""
        i, h, s = await db.get_credentials(event.chat.id)
        if i and h and s is not None:
            try:
                userbot = Client("saverestricted", session_string=s, api_hash=h, api_id=int(i))     
                await userbot.start()
            except Exception as e:
                print(e)
                if "AUTH_KEY_UNREGISTERED" in str(e):
                     return edit.edit("⚠️ Please /logout and /login again.")
                if "SESSION_REVOKED" in str(e):
                     return edit.edit("⚠️ You terminated your session, please /logout and /login again.")
                else:
                     return await edit.edit(str(e))
        else:
            return await edit.edit("⚠️ Please /login in order to use this bot.")
        await db.update_process(event.sender_id)
        process += 1
        try: 
            await get_msg(userbot, Bot, Drone,event.sender_id, to, edit.id, link, 0)
        except Exception as e:
            print(e)
            pass
        await userbot.stop()
        process -= 1
        await db.update_trial_count(event.sender_id)
        await Drone.send_message(event.sender_id, "**Check this 🔥\n\nt.me/DroneBots/3**")
        await set_timer(Drone, event.sender_id, ut)
        return
    if 't.me' in link:
        await db.update_process(event.sender_id)
        try:
            await get_msg(None, Bot, Drone, event.sender_id, to, edit.id, link, 0)
        except Exception as e:
            print(e)
            pass
        await set_timer(Drone, event.sender_id, ut)
        await Drone.send_message(event.sender_id, "**Check this 🔥\n\nt.me/DroneBots/3**")
        # return edit.edit(str("⚠️ Public channel links are only for Paid users, check @Dronebots"))

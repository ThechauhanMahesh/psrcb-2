# Github.com/Vasusen-code

import logging
from .. import CustomBot, bot as Drone

from main.plugins.helpers import get_link, check_subscription, set_timer
from main.Database.database import db
from main.plugins.pyroplug import get_msg
from main.plugins.batch import batch_link

from pyrogram import Client, filters, types

message = "Send me the message link you want to start saving from, as a reply to this message."
     
errorC = """Error: Couldn't start client by Login credentials, Please logout and login again."""

ONGOING = 0

@Drone.on_message(filters=filters.private & filters.incoming, group=2)
async def clone(client, message: types.Message):
    global ONGOING
    if batch_link:
        return
    user_id = message.from_user.id
    try:
        link = get_link(message.text)
        if not link:
            return
    except TypeError:
        return
    await check_subscription(user_id)
    data = await db.get_data(user_id)
    plan = data["plan"]
    if data["dos"] is None:
        await message.reply("⚠️ You are not subscribed to premium bot, pay in @SubscriptionForBot to buy.")
        return
    edit = await message.reply("Processing!")
    if (await db.get_process(user_id))["process"] == True:
        return await edit.edit("❌ Please don't spam links, wait until ongoing process is done.")
    if ONGOING >= 10:
         return await edit.edit("This bot is full with 10/10 users, try another bot from list pinned in @Premium_SRCB")
    to = await db.get_chat(user_id)
    if to is None:
        to = user_id
    if 't.me/+' in link:
        return await edit.edit("Join yourself manually.")
    if 't.me' in link:
        userbot = ""
        i, h, s = await db.get_credentials(user_id)
        if not s:
            return await edit.edit("⚠️ Your login credentials not found.")
        try:
            userbot = CustomBot(f"sr_{user_id}", session_string=s, api_hash=h, api_id=int(i))     
            await userbot.start()
        except Exception as e:
            logging.exception(e)
            return await edit.edit(str(e))
        await db.update_process(user_id)
        ONGOING += 1
        caption_data = await db.get_caption(user_id)
        try: 
            await get_msg(userbot, client, user_id, to, edit, link, caption_data, retry=0, plan=plan)
            await userbot.stop()
        except Exception as e:
            logging.exception(e)
            await message.reply(f"An error occurred: {e}")
        timer = 2 if plan == "pro" else 10
        await set_timer(client, user_id, timer) 
        ONGOING -= 1

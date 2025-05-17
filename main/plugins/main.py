# Github.com/Vasusen-code

import logging
import time
from .. import CustomBot, bot as Drone, TIME_LIMIT, DAILY_LIMIT

from main.plugins.helpers import get_link, check_subscription
from main.Database.database import db
from main.plugins.pyroplug import get_msg
from main.plugins.batch import batch_link

from pyrogram import Client, filters, types

message = "Send me the message link you want to start saving from, as a reply to this message."
     
errorC = """Error: Couldn't start client by Login credentials, Please logout and login again."""

@Drone.on_message(filters=filters.private & filters.incoming, group=2)
async def clone(client, message: types.Message):
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
    if data["dos"] and plan != "free":
        await message.reply("⚠️ You are already subscribed to premium bot, please use bot from @premium_srcb")
        return
    edit = await message.reply("Processing!")

    process = await db.get_process(user_id)
    if process["process"] == True:
        return await edit.edit("❌ Please don't spam links, wait until ongoing process is done.")
    if process["used"] > DAILY_LIMIT:
        return await edit.edit("❌ Daily limit exceeded, please try again tomorrow or upgrade your plan.")
    if time.time() - process["time"] < TIME_LIMIT:
        return await edit.edit("❌ Please don't spam links, wait {} seconds.".format(int(TIME_LIMIT - (time.time() - process["time"]))))
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
        caption_data = await db.get_caption(user_id)
        try: 
            await get_msg(userbot, client, user_id, to, edit, link, caption_data, retry=0, plan=plan)
            await userbot.stop()
        except Exception as e:
            logging.exception(e)
            await message.reply(f"An error occurred: {e}")
        await db.rem_process(user_id) #also updates the process time
        await message.reply("You can start new process after {} minutes.".format(int(TIME_LIMIT/60)))
        return

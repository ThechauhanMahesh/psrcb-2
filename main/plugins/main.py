# Github.com/Vasusen-code

from .. import bot as Drone
from .. import AUTH_USERS 

from main.plugins.helpers import get_link, check_subscription, set_timer
from main.Database.database import db
from main.plugins.pyroplug import get_msg
from main.plugins.batch import batch_link

from pyrogram import Client, filters, types

import asyncio

message = "Send me the message link you want to start saving from, as a reply to this message."
     
errorC = """Error: Couldn't start client by Login credentials, Please logout and login again."""

@Drone.on_message(filters=filters.command('free') & filters.incoming)
async def free(_, message: types.Message):
    user_id = message.from_user.id
    if not (await db.get_process(user_id))["process"]:
        return
    if (await db.get_process(user_id))["batch"]:
        return await message.reply("Use /cancel to stop batch.")
    await message.reply("Done, try after 10 minutes.")
    await asyncio.sleep(600)
    return await db.rem_process(user_id)

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
    s = await db.get_data(user_id)
    if s["dos"] == None:
        await message.reply("⚠️ You are not subscribed to premium bot, pay in @SubscriptionForBot to buy.")
        return
    edit = await message.reply("Processing!")
    if (await db.get_process(user_id))["process"] == True:
        return await edit.edit("❌ Please don't spam links, wait until ongoing process is done.")
    timer = 10
    if (await db.get_data(user_id))["plan"] == "pro":
        timer = 2
    to = await db.get_chat(user_id)
    if to == None:
        to = user_id
    if 't.me/+' in link:
        return await edit.edit("Join yourself manually.")
    if 't.me' in link:
        userbot = ""
        i, h, s = await db.get_credentials(user_id)
        if s:
            try:
                userbot = Client("saverestricted", session_string=s, api_hash=h, api_id=int(i))     
                await userbot.start()
            except Exception as e:
                print(e)
                return await edit.edit(str(e))
        else:
            return await edit.edit("⚠️ Your login credentials not found.")
        await db.update_process(user_id)
        try: 
            await get_msg(userbot, client, user_id, to, edit, link, i=0)
            await userbot.stop()
        except Exception as e:
            print(e)
            pass
        await set_timer(client, user_id, timer) 

#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
Plugin for both public & private channels!
"""

import asyncio
import logging

from .. import CustomBot, bot as Drone, AUTH_USERS
#from main.plugins.main import ONGOING
from main.plugins.pyroplug import get_msg
from main.plugins.helpers import extract_tg_link, get_link, rreplace, set_subscription, check_subscription
from main.Database.database import db

from pyrogram import filters, types
from pyrogram.errors import FloodWait, FloodPremiumWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyromod.exceptions import ListenerTimeout

errorC = """Error: Couldn't start client by Login credentials, Please logout and login again."""

batch_link = False

@Drone.on_message(filters=filters.command('cancel') & filters.incoming)
async def cancel(_, message: types.Message):
    if not (await db.get_process(message.from_user.id))["batch"]:
        return await message.reply("No batch active, all previous conversations are cancelled.")
    await db.rem_process(message.from_user.id)
    await message.reply("✅ Done.")

@Drone.on_message(filters=filters.command('myplan') & filters.incoming)
async def myplan(_, message: types.Message):
    data = await db.get_data(message.from_user.id)
    await message.reply(f'**DATE OF SUBSCRIPTION:** {data["dos"]}\n**DATE OF EXPIRY:** {data["doe"]}\n**PLAN:** {data["plan"]}')
    return

@Drone.on_message(filters=filters.command('x') & filters.incoming)
async def ss(_, message: types.Message):
    if message.from_user.id not in AUTH_USERS:
        return 
    edit = await message.reply("Processing...")
    msg = message.reply_to_message
    data = str(msg.text).split(" ")
    date = data[1]
    if date == "None":
        date = False
    await set_subscription(int(data[0]), date, int(data[2]), data[3])
    x = await db.get_data(int(data[0]))
    await edit.edit(f'{x}')
    await Drone.send_message(int(data[0]), "Your plan is successfully active ✅\n\nCheck @Premium_SRCB for paid bots ⚡️")


@Drone.on_message(filters=filters.command('caption') & filters.incoming)
async def caption(_, message: types.Message):
    if (await db.get_data(message.from_user.id))["plan"] != "pro":
        return await message.reply("⚠️ Purchase pro plan.")
    await message.reply(
        "Choose an action", 
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("OFF", "off")],
                [InlineKeyboardButton("ADD", "add")],
                [InlineKeyboardButton("DELETE", "delete")],
                [InlineKeyboardButton("REPLACE", "replace")]
            ]
        )
    )

@Drone.on_callback_query(filters.regex(r"add"))
async def add(_, cb: CallbackQuery):
    await cb.message.delete()
    user_id = cb.from_user.id
    try:
        add = await Drone.ask(chat_id=user_id, text="Send the text you want to add in captions.", filters=filters.text, timeout=60)
    except ListenerTimeout:
        return await Drone.send_message(user_id, "You took too long to respond.")
    await db.add_caption(user_id, add.text)
    await Drone.send_message(user_id, "Done ✅")
        
@Drone.on_callback_query(filters.regex(r"delete"))
async def delete(_, cb: CallbackQuery):
    await cb.message.delete()
    user_id = cb.from_user.id
    try:
        delete = await Drone.ask(chat_id=user_id, text="Send the text you want to delete in captions.", filters=filters.text, timeout=60)
    except ListenerTimeout:
        return await Drone.send_message(user_id, "You took too long to respond.")
    await db.delete_caption(user_id, delete.text)
    await Drone.send_message(user_id, "Done ✅")
        
@Drone.on_callback_query(filters.regex(r"off"))
async def off(_, cb: CallbackQuery):
    await cb.message.delete()
    user_id = cb.from_user.id
    await db.disable_caption(user_id)
    await Drone.send_message(user_id, "No changes will be made in captions ✅")
    
@Drone.on_callback_query(filters.regex(r"replace"))
async def replace(_, cb: CallbackQuery):
    await cb.message.delete()
    user_id = cb.from_user.id
    try:
        delete = await Drone.ask(chat_id=user_id, text="Send the text you want to replace in captions.", filters=filters.text, timeout=60)
        replace = await Drone.ask(chat_id=user_id, text="Send the text you want to replace by in captions.", filters=filters.text, timeout=60)
    except ListenerTimeout:
        return await Drone.send_message(user_id, "You took too long to respond.")
    await db.replace_caption(user_id, {"d":delete.text, "a":replace.text})
    await Drone.send_message(user_id, "Done ✅")

@Drone.on_message(filters=filters.command('batch') & filters.incoming & filters.private)
async def batch(client, message: types.Message):
    global batch_link
    user_id = message.from_user.id
    data = await db.get_data(user_id)
    plan = data["plan"]
    caption_data = await db.get_caption(user_id)
    
    await check_subscription(user_id)

    if plan == "basic":
        await message.reply("⚠️ Buy Monthly subscription or Pro subscription.")
        return
    
    pr = (await db.get_process(user_id))["process"]
    if pr:
        return await message.reply("⚠️ You've already started one process, wait for it to complete!")
    
    batch_link = True
    try:
        link = await Drone.ask(chat_id=user_id, text="Send me the message link you want to start saving from.", filters=filters.text, timeout=60)
    except ListenerTimeout:
        await message.reply("You took too long to respond.")
    try:
        link = get_link(link.text)
    except Exception:
        return await message.reply("⚠️ No link found.")
    batch_link = True
    try:
        range_ = await Drone.ask(chat_id=user_id, text="Send me the number of files/range you want to save from the given message.", filters=filters.text, timeout=60)
    except ListenerTimeout:
        await message.reply("You took too long to respond.")
        batch_link = False
        return 
    batch_link = False
    try:
        range_ = range_.text
        value = int(range_)
        if value > 30:
            if not plan == "pro":
                await message.reply("⚠️ You can only get upto 30 files in a single batch.")
                return
            elif value > 100:
                await message.reply("⚠️ You can only get upto 100 files in a single batch.")
                return 
    except ValueError:
        await message.reply("Range must be an integer!")
        return
            
    i, h, s = await db.get_credentials(user_id)
    chat = await db.get_chat(user_id)
    if chat == None:
        chat = user_id
    userbot = None
    if s:
        userbot = CustomBot(f"sr_{user_id}", session_string=s, api_hash=h, api_id=int(i))     
    else:
        await message.reply("⚠️ Your login credentials not found.")
        return
    await db.update_process(user_id, batch=True)
    if ONGOING >= 10:
        return await edit.edit("This bot is full with 10/10 users, try another bot from list pinned in @Premium_SRCB")
    # ONGOING += 1
    await run_batch(userbot, client, user_id, chat, link, value, caption_data, plan) 
    await db.rem_process(user_id)
    # ONGOING -= 1
    
async def run_batch(userbot: CustomBot, client: CustomBot, sender: int, chat: int, link: str, value: int, caption_data: dict, plan: str):
    try: 
        await userbot.start()
    except Exception as e:
        print(e)
        return await client.send_message(sender, f'{errorC}\n\n**Error:** {str(e)}')
    # if chat != sender:
    #     try:
    #         await client.get_chat(chat)
    #     except Exception as e:
    #         print(e)
    #         return await client.send_message(sender, "⚠️ Chat not found, please make sure you have added me in the destination chat.")
    chat_id, msg_id = extract_tg_link(link)
    if not chat_id or not msg_id:
        await client.send_message(sender, "⚠️ Invalid link.")
    try:
        async for last_msg in userbot.get_chat_history(chat_id = chat_id, limit=1):
            break
    except Exception as e:
        logging.exception(e)
        await client.send_message(sender, f"An error occured : {e}")
    if last_msg.id < (msg_id+value):
        #await client.send_message(sender, "⚠️ Requested range is greater than the total files in the chat, sending till the last file.")
        value = last_msg.id - (msg_id-1)
    for i in range(value):
        if (await db.get_data(sender))["plan"] == "pro":
            if 't.me/c/' not in link and 't.me/b/' not in link:
                timer = 3
            else:
                timer = 2
                if i > 25 and i < 50:
                    timer = 5
                elif i > 50 and i < 100:
                    timer = 8
                elif i > 100:
                    timer = 10
        else:
            if i < 50:
                timer = 10
            elif i > 50 and i < 100:
                timer = 20
            elif i > 100:
                timer = 25
            if 't.me/c/' not in link and 't.me/b/' not in link:
                timer = 5
        try:
            if not (await db.get_process(sender))["process"]:
                await client.send_message(sender, "✅ Batch completed.")
                break
        except Exception as e:
            print(e)
            await client.send_message(sender, "✅ Batch completed.")
            break
        editable = await client.send_message(sender, "Processing...")
        new_link = rreplace(link, f"/{msg_id}", f"/{msg_id+i}")
        try:
            await get_msg(userbot, client, sender, chat, editable, new_link, caption_data, retry=0, plan=plan, is_batch=True)
        except (FloodWait, FloodPremiumWait) as fw:
            fw.value += 5 #Add 5 seconds to the floodwait time
            print(f"Sleeping for {fw.value} seconds due to Floodwait.")
            await client.send_message(sender, f"⚠️ Sleeping for `{fw.value}` seconds due to Floodwait.")
            await asyncio.sleep(fw.value)
            await get_msg(userbot, client, sender, chat, editable, new_link, caption_data, retry=1, plan=plan, is_batch=True)
            continue #Skip the next sleep
        except Exception as e:
            logging.exception(e)
            await client.send_message(sender, f"An error occured : {e}")
        protection = await client.send_message(chat, f"⚠️ Sleeping for `{timer}` seconds to avoid Floodwaits and Protect account!")
        await asyncio.sleep(timer)
        await protection.delete()
    #Stop the userbot
    await userbot.stop()
    await client.send_message(sender, "✅ Batch completed.")

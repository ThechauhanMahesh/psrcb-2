#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
Plugin for both public & private channels!
"""

import asyncio
import logging

from .. import CustomBot, bot as Drone, AUTH_USERS
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
    await message.reply("⚠️ Please use bot from @premium_srcb")
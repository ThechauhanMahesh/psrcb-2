# Github.com/Vasusen-code

import os 
from main.plugins.helpers import download, extract_tg_link, upload
from main.Database.database import db
from main import DUMP_CHANNEL
from pyrogram.enums import MessageMediaType
from pyrogram import Client

def thumbnail(sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    else:
         return None
      
async def get_msg(userbot, client: Client, sender, to, editable_msg, msg_link, caption_data, i=0, plan="basic"):
    if i >= 2:
        return await editable_msg.edit("❌ Failed to save: `{msg_link}`\n\nError: Maximum retries exceeded.")

    file, file_size, chat, caption, thumb_path = None, None, None, None, thumbnail(sender)

    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]

    chat, msg_id = extract_tg_link(msg_link)
    
    if chat and msg_id:
        try:
            msg = await userbot.get_messages(chat, msg_id)

            if msg.media:
                if msg.media==MessageMediaType.WEB_PAGE:
                    await editable_msg.edit("Cloning.")
                    await client.send_message(to, msg.text.markdown)
                    await editable_msg.delete()
                    return
                else:
                    downloaded, update = await download(userbot, msg, editable_msg)
                    if not downloaded:
                        if not update:
                            await editable_msg.delete()
                            return
                        await editable_msg.edit(f"❌ Failed to save: `{msg_link}`\n\nError: {update}")
                        return
                    else:
                        file = update
            elif msg.text:
                await editable_msg.edit("Cloning.")
                await client.send_message(to, msg.text.markdown)
                await editable_msg.delete()
                return
            else:
                return

            if msg.caption is not None:
                caption = msg.caption
                if plan == "pro":
                    new_caption = ""
                    action = caption_data["action"]
                    string = caption_data["string"]
                    if action is not None:
                        if action == "add":
                            new_caption = caption + f"\n\n{string}"
                        if action == "delete":
                            new_caption = caption.replace(string, "")
                        if action == "replace":
                            new_caption = caption.replace(string["d"], string["a"])
                        caption = new_caption
            else:
                if plan == "pro":
                    action = caption_data["action"]
                    if action == "add":
                        caption = caption_data["string"]

            await editable_msg.edit("Preparing to upload...")

            if file == None:
                return await editable_msg.edit(f'❌ Failed to save: `{msg_link}`\n\nThis link is not downloadble.')

            if os.path.getsize(file) > 2097152000:
                if plan != "pro":
                    return await editable_msg.edit("Buy pro plan and telegram premium to upload file size over 2Gb.")
                else:
                    if to == sender:
                        to = client.username
                    uploaded, update = await upload(userbot, file, to, msg, editable_msg, thumb_path=thumb_path, caption=caption)
            else:
                if is_exists:=db.get_cache(msg_id, chat):
                    uploaded = await client.copy_message(chat_id=to, from_chat_id=DUMP_CHANNEL, message_id=is_exists["cache_msg_id"])
                else:
                    uploaded, update = await upload(client.get_client(), file, DUMP_CHANNEL, msg, editable_msg, thumb_path=thumb_path, caption=caption)
                    if uploaded and update:
                        await db.save_cache(msg_id, chat, uploaded.id)

            if uploaded:
                await editable_msg.delete()
            else:
                if not update:
                    return await get_msg(userbot, client, sender, to, editable_msg, msg_link, caption_data, i=i, plan=plan)
                else:
                    return await editable_msg.edit(f"❌ Failed to upload: `{msg_link}`\n\nError: {update}")
                    
        except Exception as e:
            print(e)
            return await editable_msg.edit(f'❌ Failed to save: `{msg_link}`\n\nError: {str(e)}')

        await editable_msg.delete()
    else:
        await editable_msg.edit(f'❌ Failed to save: `{msg_link}`\n\nError: Invalid link.')

        
async def get_bulk_msg(userbot, client, sender, to, msg_link, caption_data, i=0, plan="basic"):
    x = await client.send_message(sender, "Processing!")
    return await get_msg(userbot, client, sender, to, x, msg_link, caption_data, i=i, plan=plan)

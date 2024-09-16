# Github.com/Vasusen-code

import logging
import os 
from main.plugins.helpers import build_caption, download, extract_tg_link, upload
from main.Database.database import db
from main import DUMP_CHANNEL
from pyrogram.enums import MessageMediaType
from pyrogram import Client

def thumbnail(sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    else:
         return None
      
async def get_msg(userbot, client: Client, sender, to, editable_msg, msg_link, caption_data, retry=0, plan="basic", is_batch=False):
    if retry >= 3:
        return await editable_msg.edit(f"❌ Failed to save: `{msg_link}`\n\nError: Maximum retries exceeded.")

    file, caption, thumb_path = None, None, thumbnail(sender)

    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]

    chat, msg_id = extract_tg_link(msg_link)
    if cache_file := await db.get_cache(msg_id, chat):
        caption = build_caption(plan, caption=cache_file["caption"] or "", caption_data=caption_data)
        await client.copy_message(chat_id=to, from_chat_id=DUMP_CHANNEL, message_id=cache_file["msg_id"], caption=caption)
        await editable_msg.delete()
        return

    if chat and msg_id:
        try:
            try:
                msg = await userbot.get_messages(chat, msg_id)
                if msg.empty:
                    raise Exception("Message deleted or not exist.")
            except Exception as e:
                if is_batch:
                    return await editable_msg.delete()
                return await editable_msg.edit(f'❌ Failed to save: `{msg_link}`\n\nError: {str(e)}')
            if msg.media:
                if msg.media==MessageMediaType.WEB_PAGE:
                    await editable_msg.edit("Cloning.")
                    await client.send_message(to, msg.text.markdown)
                    await editable_msg.delete()
                    return
                else:
                    downloaded, update = await download(userbot, msg, editable_msg)
                    if not downloaded:
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

            caption = build_caption(plan, msg.caption, caption_data)

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
                up_client = client.get_client()
                if not up_client:
                    return await editable_msg.edit("❌ Failed to save: `{msg_link}`\n\nError: No clients available to use.")
                uploaded, update = await upload(up_client["client"], file, DUMP_CHANNEL, msg, editable_msg, thumb_path=thumb_path, caption=caption)
                if uploaded and update:
                    await db.save_cache(msg_id, chat, update.id, msg.caption.markdown if msg.caption else "")
                await client.copy_message(chat_id=to, from_chat_id=DUMP_CHANNEL, message_id=update.id)
                client.release_client(up_client)

            if uploaded:
                await editable_msg.delete()
            else:
                if not update:
                    return await get_msg(userbot, client, sender, to, editable_msg, msg_link, caption_data, retry=retry, plan=plan, specified_msg_id=msg_id, is_batch=is_batch)
                else:
                    return await editable_msg.edit(f"❌ Failed to upload: `{msg_link}`\n\nError: {update}")

        except Exception as e:
            logging.exception(e)
            return await editable_msg.edit(f'❌ Failed to save: `{msg_link}`\n\nError: {str(e)}')

        await editable_msg.delete()
    else:
        await editable_msg.edit(f'❌ Failed to save: `{msg_link}`\n\nError: Invalid link.')


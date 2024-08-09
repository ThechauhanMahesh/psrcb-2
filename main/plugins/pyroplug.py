# Github.com/Vasusen-code

import os 

from main.plugins.helpers import download, upload

from pyrogram.enums import MessageMediaType
from pyrogram import Client

def thumbnail(sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    else:
         return None
      
async def get_msg(userbot, client:Client, sender, to, editable_msg, msg_link, caption_data, i=0, plan="basic"):

    file, file_size, chat, caption, thumb_path, upload_client = None, None, None, None, thumbnail(sender), client

    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]

    msg_id = int(msg_link.split("/")[-1]) + int(i)
    
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
        if 't.me/b/' in msg_link:
            chat = str(msg_link.split("/b/")[1].split("/")[0])
        elif 't.me/c/' in msg_link:
            chat = int('-100' + str(msg_link.split("/c/")[1]).split("/")[0])
        try:
            msg = await userbot.get_messages(chat, msg_id)
            
            if not msg.media:
                if msg.text:
                    await editable_msg.edit("Cloning.")
                    await client.send_message(to, msg.text.markdown)
                    await editable_msg.delete()
                    return
                
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
                
            file_size = os.path.getsize(file)
            
            if file_size > 2097152000:
                if plan != "pro":
                    return await editable_msg.edit("Buy pro plan and telegram premium to upload file size over 2Gb.")
                else:
                    upload_client = userbot
                    if to == sender:
                        me = await client.get_me()
                        to = me.username
            
            uploaded, update = await upload(upload_client, file, to, msg, editable_msg, thumb_path=thumb_path, caption=caption)
            if uploaded:
                await editable_msg.delete()
            else:
                if not update:
                    return await get_msg(userbot, client, sender, to, editable_msg, msg_link, caption_data, i=0, plan=plan)
                else:
                    return await editable_msg.edit(f"❌ Failed to upload: `{msg_link}`\n\nError: {update}")
                    
        except Exception as e:
            print(e)
            return await editable_msg.edit(f'❌ Failed to save: `{msg_link}`\n\nError: {str(e)}')
            
        await editable_msg.delete()

    else:
        await editable_msg.edit("Cloning.")

        chat =  msg_link.split("me/")[1].split("/")[0]

        try:
            msg = await client.get_messages(chat, msg_id)
            if msg.empty:
                group_link = f't.me/b/{chat}/{int(msg_id)}'
                return await get_msg(userbot, client, sender, to, editable_msg, group_link, caption_data, i=0, plan=plan)
            else:
                await client.copy_message(to, chat, msg_id)
        except Exception as e:
            print(e)
            return await editable_msg.edit(f'❌ Failed to clone: `{msg_link}`\n\nError: {str(e)}')
        
        await editable_msg.delete()
     

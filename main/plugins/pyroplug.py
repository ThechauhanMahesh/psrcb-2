# Github.com/Vasusen-code

import os 

from main.plugins.helpers import download, upload
from main.Database.database import db

from pyrogram.enums import MessageMediaType

from main.Database.database import db

def thumbnail(sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    else:
         return None
      
async def get_msg(userbot, client, sender, to, editable_msg, msg_link, i=0):

    file, chat, caption, thumb_path = None, None, None, thumbnail(sender)
    plan = await db.get_data(sender)["plan"]

    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]

    msg_id = int(msg_link.split("/")[-1]) + int(i)
    
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
        if 't.me/b/' in msg_link:
            chat = str(msg_link.split("/")[-2])
        else:
            chat = int('-100' + str(msg_link.split("/")[-2]))

        try:
            msg = await userbot.get_messages(chat, msg_id)

            # check file size here

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
                        await editable_msg.edit(f"❌ Failed to save: `{msg_link}`\n\Error: {update}")
                        return
                    else:
                        file = update

            if msg.caption is not None:
                caption = msg.caption
                if plan == "pro":
                    new_caption = ""
                    caption_data = await db.get_caption(sender)
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
                    caption_data = await db.get_caption(sender)
                    action = caption_data["action"]
                    if action == "add":
                        caption = caption_data["string"]

            await editable_msg.edit("Preparing to upload...")
            uploaded, update = await upload(client, file, to, msg, editable_msg, thumb_path=thumb_path, caption=caption)
            if uploaded:
                await editable_msg.delete()
            else:
                if not update:
                    return await get_msg(userbot, client, sender, to, editable_msg, msg_link, i=0)
                else:
                    await editable_msg.edit(f"❌ Failed to upload: `{msg_link}`\n\Error: {update}")
                
            try:
                os.remove(file)
            except:
                pass
        except Exception as e:
            pass

        await editable_msg.delete()

    else:
        await editable_msg.edit("Cloning.")

        chat =  msg_link.split("me/")[1].split("/")[0]

        try:
            msg = await client.get_messages(chat, msg_id)
            if msg.empty:
                group = await userbot.get_chat(chat)
                group_link = f't.me/c/{int(group.id)}/{int(msg_id)}'
                return await get_msg(userbot, client, sender, to, editable_msg, group_link, i=i)
            else:
                await client.copy_message(to, chat, msg_id)
        except Exception as e:
            print(e)
            return await editable_msg.edit(f'❌ Failed to clone: `{msg_link}`\n\nError: {str(e)}')
        
        await editable_msg.delete()
     
        
async def get_bulk_msg(userbot, client, sender, to, msg_link, i=0):
    x = await client.send_message(sender, "Processing!")
    await get_msg(userbot, client, sender, to, x, msg_link, i=i)

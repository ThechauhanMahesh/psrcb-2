# Github.com/Vasusen-code

from .. import bot as Drone, BOT_UN, uploader_ubot
import asyncio, time, os, shutil, datetime 

from main.plugins.progress import progress_for_pyrogram
from main.plugins.helpers import screenshot, findVideoResolution
from main.plugins.helpers import duration as dr
from main.Database.database import db

from pyrogram import Client, filters
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.enums import MessageMediaType, ChatType
from ethon.pyfunc import video_metadata
from ethon.telefunc import fast_upload
from telethon.tl.types import DocumentAttributeVideo
from telethon import events

from main.Database.database import db

def thumbnail(sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    else:
         return None
      
async def get_msg(userbot, client, bot, sender, to, edit_id, msg_link, i):
    edit = ""
    chat = ""
    round_message = False
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    msg_id = int(msg_link.split("/")[-1]) + int(i)
    height, width, duration, thumb_path = 90, 90, 0, None
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
        if 't.me/b/' in msg_link:
            chat = str(msg_link.split("/")[-2])
        else:
            chat = int('-100' + str(msg_link.split("/")[-2]))
        file = ""
        try:
            msg = await userbot.get_messages(chat, msg_id)
            if msg.media:
                if msg.media==MessageMediaType.WEB_PAGE:
                    edit = await client.edit_message_text(sender, edit_id, "Cloning.")
                    await client.send_message(to, msg.text.markdown)
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    edit = await client.edit_message_text(sender, edit_id, "Cloning.")
                    await client.send_message(to, msg.text.markdown)
                    await edit.delete()
                    return
            edit = await client.edit_message_text(sender, edit_id, "Trying to Download.")
            try:
                file = await userbot.download_media(
                    msg,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        "**🔻 DOWNLOADING:**\n",
                        edit,
                        time.time()
                    )
                )
            except FileNotFoundError:
                new_name = file.split("downloads/")[1].replace("/", "-")
                file = await userbot.download_media(
                    msg,
                    file_name=new_name,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        "**🔻 DOWNLOADING:**\n",
                        edit,
                        time.time()
                    )
                )
            print(file)
            await edit.edit('Preparing to Upload!')
            caption = None
            if msg.caption is not None:
                caption = msg.caption
                if (await db.get_data(sender))["plan"] == "pro":
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
                if (await db.get_data(sender))["plan"] == "pro":
                    caption_data = await db.get_caption(sender)
                    action = caption_data["action"]
                    if action == "add":
                        caption = caption_data["string"]
            if msg.media==MessageMediaType.VIDEO_NOTE:
                round_message = True
                print("Trying to get metadata")
                data = video_metadata(file)
                height, width, duration = data["height"], data["width"], data["duration"]
                print(f'd: {duration}, w: {width}, h:{height}')
                try:
                    thumb_path = await screenshot(file, duration, sender)
                except Exception:
                    thumb_path = None
                await client.send_video_note(
                    chat_id=to,
                    video_note=file,
                    length=height, duration=duration, 
                    thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        '**🔺 UPLOADING:**\n',
                        edit,
                        time.time()
                    )
                )
            elif msg.media==MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"] or file.split(".")[-1].lower() in ["mp4", "mkv"]:
                print("Trying to get metadata")
                data = video_metadata(file)
                height, width, duration = data["height"], data["width"], data["duration"]
                print(f'd: {duration}, w: {width}, h:{height}')
                try:
                    thumb_path = await screenshot(file, duration, sender)
                except Exception:
                    thumb_path = None
                await client.send_video(
                    chat_id=to,
                    video=file,
                    caption=caption,
                    supports_streaming=True,
                    height=height, width=width, duration=duration, 
                    thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        '**🔺 UPLOADING:**\n',
                        edit,
                        time.time()
                    )
                )
            elif msg.media==MessageMediaType.VOICE:
                await client.send_voice(to, file, caption=caption)
                
            elif msg.media==MessageMediaType.PHOTO:
                await edit.edit("🔺 Uploading photo...")
                await bot.send_file(to, file, caption=caption)
            else:
                thumb_path=thumbnail(sender)
                await client.send_document(
                    to,
                    file, 
                    caption=caption,
                    thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        '**🔺 UPLOADING:**\n',
                        edit,
                        time.time()
                    )
                )
            try:
                os.remove(file)
                if os.path.isfile(file) == True:
                    os.remove(file)
            except Exception as e:
                print(e)
            await edit.delete()
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await client.edit_message_text(sender, edit_id, "⚠️ Have you joined the channel?")
            return
        except PeerIdInvalid:
            chat = msg_link.split("/")[-3]
            try:
                int(chat)
                new_link = f"t.me/c/{chat}/{msg_id}"
            except:
                new_link = f"t.me/b/{chat}/{msg_id}"
            return await get_msg(userbot, client, bot, sender, to, edit_id, new_link, i)
        except Exception as e:
            print(e)
            if "This message doesn't contain any downloadable media" in str(e):
                pass
            elif "size equals" in str(e) \
            or "SaveBigFilePartRequest" in str(e):
                await asyncio.sleep(60)
                try:
                    os.remove(file)
                except:
                    pass
                return await get_msg(userbot, client, bot, sender, to, edit_id, msg_link, i)
            elif "messages.SendMedia" in str(e) \
            or "SendMediaRequest" in str(e):
                try:
                    if msg.media==MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:
                            UT = time.time()
                            uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**🔺 UPLOADING:**')
                            attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, round_message=round_message, supports_streaming=True)] 
                            await bot.send_file(to, uploader, caption=caption, thumb=thumb_path, attributes=attributes, force_document=False)
                    elif msg.media==MessageMediaType.VIDEO_NOTE:
                        uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**🔺 UPLOADING:**')
                        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, round_message=round_message, supports_streaming=True)] 
                        await bot.send_file(to, uploader, caption=caption, thumb=thumb_path, attributes=attributes, force_document=False)
                    else:
                        UT = time.time()
                        uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**🔺 UPLOADING:**')
                        await bot.send_file(to, uploader, caption=caption, thumb=thumb_path, force_document=True)
                    if os.path.isfile(file) == True:
                        os.remove(file)
                except exception as e:
                    print("Tried telethon but failed because ", e)
                    return await client.edit_message_text(sender, edit_id, f'❌ Failed to save: `{msg_link}`\n\nError: {str(e)}')
            elif "2000" in str(e):
                try:
                    if not (await db.get_data(sender))["plan"] == "pro":
                        try:
                            os.remove(file)
                        except Exception:
                            pass 
                        return await client.edit_message_text(sender, edit_id, f'❌ Failed to save: `{msg_link}`\n\nPurchase pro plan to save 2gb+ files.')
                    if msg.media==MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:
                        print("Trying to get metadata")
                        data = video_metadata(file)
                        height, width, duration = data["height"], data["width"], data["duration"]
                        print(f'd: {duration}, w: {width}, h:{height}')
                        try:
                            thumb_path = await screenshot(file, duration, sender)
                        except Exception:
                            thumb_path = None
                        bigfilemsg = await uploader_ubot.send_video(chat_id="bigsizecontent", video=file, caption=caption, 
                                                supports_streaming=True, 
                                                height=height, width=width, duration=duration, 
                                                thumb=thumb_path,
                                                progress=progress_for_pyrogram,
                                                progress_args=(
                                                    client,
                                                    '**🔺 UPLOADING:**\n',
                                                    edit,
                                                    time.time()))
                        
                    else:
                        thumb_path=thumbnail(sender)
                        bigfilemsg = await uploader_ubot.send_document(
                            "bigsizecontent",
                            file, 
                            caption=caption,
                            thumb=thumb_path,
                            progress=progress_for_pyrogram,
                            progress_args=(
                                client,
                                '**🔺 UPLOADING:**\n',
                                edit,
                                time.time()
                            )
                        )
                    await client.copy_message(to, chat, bigfilemsg.id)
                    await bigfilemsg.delete()
                except Exception as e:
                    if "SaveBigFilePartRequest" in str(e):
                        await client.edit_message_text(sender, edit_id, f'FILE from `{msg_link}` has been uploaded in your saved messages.')
                    else:
                        await client.edit_message_text(sender, edit_id, f'❌ Failed to save: `{msg_link}`\n\nError: {str(e)}')
                        try:
                            os.remove(file)
                        except Exception:
                            return
                        return 
            else:
                await client.edit_message_text(sender, edit_id, f'❌ Failed to save: `{msg_link}`\n\nError: {str(e)}')
                try:
                    os.remove(file)
                except Exception:
                    return
                return
        try:
            os.remove(file)
        except Exception:
            pass
        await edit.delete()
    else:
        edit = await client.edit_message_text(sender, edit_id, "Cloning.")
        chat =  msg_link.split("t.me")[1].split("/")[1]
        try:
            msg = await client.get_messages(chat, msg_id)
            if msg.empty:
                i, h, s = await db.get_credentials(sender)
                if i and h and s is not None:
                    try:
                        userbot = Client("saverestricted", session_string=s, api_hash=h, api_id=int(i))     
                        await userbot.start()
                    except Exception as e:
                        print(e)
                        return await edit.edit(str(e))
                else:
                    return await edit.edit("⚠️ Your login credentials not found.")
                group = await userbot.get_chat(chat)
                group_link = f't.me/c/{int(group.id)}/{int(msg_id)}'
                await get_msg(userbot, client, bot, sender, to, edit_id, msg_link, i)
                return await userbot.stop()
            await client.copy_message(to, chat, msg_id)
        except Exception as e:
            print(e)
            return await client.edit_message_text(sender, edit_id, f'❌ Failed to save: `{msg_link}`\n\nError: {str(e)}')
        await edit.delete()
     
        
async def get_bulk_msg(userbot, client, sender, chat, msg_link, i):
    x = await client.send_message(sender, "Processing!")
    await get_msg(userbot, client, Drone, sender, chat, x.id, msg_link, i)

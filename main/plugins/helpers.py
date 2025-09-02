#Github.com/Vasusen-code
import logging
import subprocess
import shlex
import json
from datetime import timedelta
from datetime import date
from datetime import datetime as dt
import asyncio, subprocess, re, os, time
import uuid
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait, InviteHashInvalid, InviteHashExpired, UserAlreadyParticipant, FloodPremiumWait
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.errors import UserNotParticipant, MessageNotModified
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from main.plugins.progress import progress_for_pyrogram
from main.Database.database import db
from main import DL_DIR, SPLIT_SIZE, CustomBot


AUDIO_SUFFIXES = ("MP3", "M4A", "M4B", "FLAC", "WAV", "AIF", "OGG", "AAC", "DTS", "MID", "AMR", "MKA")
VIDEO_SUFFIXES = ("M4V", "MP4", "MOV", "FLV", "WMV", "3GP", "MPG", "WEBM", "MKV", "AVI")


def check_is_streamable(file_path:str) -> bool:
    return file_path.upper().endswith(VIDEO_SUFFIXES)

def check_is_audio(file_path:str) -> bool:
    return file_path.upper().endswith(AUDIO_SUFFIXES)

def ffmpeg_split(file_path:str) -> bool:
    return check_is_streamable(file_path) or check_is_audio(file_path)

def delete_file(file):
    try:
        os.remove(file)
        if os.path.isfile(file):
            os.remove(file)
    except:
        pass

def rreplace(s, old, new):
    return s[::-1].replace(old[::-1], new[::-1], 1)[::-1]

def build_caption(plan, caption, caption_data):
    if plan == "pro":
        action = caption_data["action"]
        if caption is not None:
            new_caption = ""
            if action is not None:
                string = caption_data["string"]
                if action == "add":
                    new_caption = caption + f"\n\n{string}"
                elif action == "delete":
                    new_caption = caption.replace(string, "")
                elif action == "replace":
                    new_caption = caption.replace(string["d"], string["a"])
                caption = new_caption
        elif action == "add":
            caption = caption_data["string"] or ""
    return caption

# TG Link extractor -----------------------------------------------------------------------------------
def extract_tg_link(url):
    if not isinstance(url, str):
        logging.error(f"URL must be a string, {url} given.")
        return None, None
    pattern = r"^(?:(?:https|tg):\/\/)?(?:www\.)?(?:t\.me\/)?(?:(?:c\/(\d+))|(?:b\/)?(\w+)|(?:openmessage\?user_id\=(\d+)))(?:\/|&message_id\=)(\d+)(?:\/(\d+))?(\?single)?$"
    if match := re.search(pattern, url.strip()):
        chat_id = None
        msg_id = int(match.group(4))
        if match.group(1):
            chat_id = int("-100" + match.group(1))
        elif match.group(2):
            chat_id = match.group(2)
        elif match.group(3):
            chat_id = int(match.group(3))
        if match.group(5):
            msg_id = int(match.group(5))
        if chat_id and msg_id:
            return chat_id, msg_id
    return None, None

# Subscription ----------------------------------------------------------------------------------

async def check_subscription(id):
    try: 
        doe = (await db.get_data(id))["doe"]
    except Exception:
        return
    if not doe:
        return
    z = doe.split("-")
    e = int(z[0] + z[1] + z[2])
    x = str(dt.now()).split(" ")[0]
    w = x.split("-")
    today = int(w[0] + w[1] + w[2])
    if today > e:
        await db.rem_data(id)
    else:
        return 

async def set_subscription(user_id, dos, days, plan):
    if not dos:
        x = str(dt.now()).split(" ")[0]
        dos_ = x.split("-")
    else:
        dos_ = dos.split("-")
    today = date(int(dos_[0]), int(dos_[1]), int(dos_[2]))
    expiry_date = today + timedelta(days=days)
    data = {"dos":str(today), "doe":str(expiry_date), "plan":plan}
    await db.update_data(user_id, data)

#Multi client-------------------------------------------------------------------------------------------------------------

async def login_credentials(sender, i, h, s):
    await db.update_api_id(sender, i)
    await db.update_api_hash(sender, h)
    await db.update_session(sender, s)
    
async def logout_credentials(sender):
    await db.rem_api_id(sender)
    await db.rem_api_hash(sender)
    await db.rem_session(sender)

#Anti-Spam---------------------------------------------------------------------------------------------------------------

#Set timer to avoid spam
async def set_timer(bot, sender, t):
    await bot.send_message(sender, f'You can start a new process again after {t} seconds.')
    await asyncio.sleep(int(t))
    await db.rem_process(sender)

#Forcesub -----------------------------------------------------------------------------------

async def force_sub(client: CustomBot, channel, id):
    s, r = False, None
    try:
        # In Pyrogram, IDs should be directly usable, so ensure 'id' is integer if not handled externally.
        x = await client.get_chat_member(channel, id)
        
        # Check if the participant has left the channel
        if x.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            s, r = True, f"To use this bot you must JOIN @{channel}"
        else:
            s, r = False, None
    except UserNotParticipant:
        s, r = True, f"To use this bot you must JOIN @{channel}"
    except Exception as e:
        s, r = True, f"ERROR: Add in ForceSub channel, or check your channel id. Details: {str(e)}"
    return s, r


#Join private chat-------------------------------------------------------------------------------------------------------------

async def join(client: CustomBot, invite_link):
    try:
        await client.join_chat(invite_link)
        return "Successfully joined the Channel"
    except UserAlreadyParticipant:
        return "User is already a participant."
    except (InviteHashInvalid, InviteHashExpired):
        return "Could not join. Maybe your link is expired or Invalid."
    except (FloodWait, FloodPremiumWait):
        return "Too many requests, try again later."
    except Exception as e:
        print(e)
        return "Could not join, try joining manually."
        
#Regex---------------------------------------------------------------------------------------------------------------
#to get the url from event

def get_link(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)
    try:
        return link if (link := [x[0] for x in url][0]) else False
    except Exception:
        return False
    
# screenshot ---------------------------------------------------------------------------------------------------------------
    
def hhmmss(seconds):
    x = time.strftime('%H:%M:%S',time.gmtime(seconds))
    return x

async def screenshot(video, duration):
    # if os.path.exists(f'{sender}.jpg'):
    #     return f'{sender}.jpg'
    time_stamp = hhmmss(int(duration)/2)
    out = dt.now().isoformat("_", "seconds") + ".jpg"
    cmd = ["ffmpeg",
           "-ss",
           f"{time_stamp}", 
           "-i",
           f"{video}",
           "-frames:v",
           "1", 
           f"{out}",
           "-y"
          ]
    await run_comman_d(cmd)
    if os.path.isfile(out):
        return out
    else:
        None

# metadata ---------------------------------------------------------------------------------------------------------------
 
# function to find the metadata of the input video file
async def findVideoMetadata(pathToInputVideo):

    height, width, duration_seconds = 90, 90, 0

    try:
        metadata = extractMetadata(createParser(pathToInputVideo))
        if metadata and metadata.has("duration"):
            duration_seconds = metadata.get("duration").seconds
            try:
                thumb = await screenshot(pathToInputVideo, duration_seconds)
            except:
                thumb = None
            if thumb != None:
                metadata = extractMetadata(createParser(thumb))
                if metadata and metadata.has("width"):
                    width = metadata.get("width")
                if metadata and metadata.has("height"):
                    height = metadata.get("height")
        else:
            cmd = "ffprobe -v quiet -print_format json -show_streams"
            args = shlex.split(cmd)
            args.append(pathToInputVideo)
            # run the ffprobe process, decode stdout into utf-8 & convert to JSON
            ffprobeOutput = subprocess.check_output(args).decode('utf-8')
            ffprobeOutput = json.loads(ffprobeOutput)

            # find height and width
            height = ffprobeOutput['streams'][0]['height']
            width = ffprobeOutput['streams'][0]['width']

            # find duration
            out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", pathToInputVideo])
            ffprobe_data = json.loads(out)
            duration_seconds = float(ffprobe_data["format"]["duration"])
    except:
        return 90, 90, 0

    return int(height), int(width), int(duration_seconds)

async def split_large_files(path, size=None, file_=None, dirpath=None, split_size=SPLIT_SIZE, listener=None, start_time=0, i=1, inLoop=False, noMap=False):
    if listener == 'cancelled' or listener is not None and listener.returncode == -9:
        return False, None
    if file_ in None:
        file_ = os.path.basename(path)
    if size is None:
        size = os.path.getsize(path)
    if dirpath is None:
        working_directory = os.path.dirname(os.path.abspath(path))
        dirpath = os.path.join(working_directory, str(time.time()))
        os.makedirs(dirpath)
    parts = -(-size // SPLIT_SIZE)
    if size <= 4600870912:
        if not inLoop:
            split_size = ((size + parts - 1) // parts) + 1000
    if ffmpeg_split(path):
        duration = (await findVideoMetadata(path))[2]
        base_name, extension = os.path.splitext(file_)
        split_size -= 1000000
        while i <= parts or start_time < duration - 4:
            parted_name = f"{base_name}.part{i:03}{extension}"
            out_path = os.path.join(dirpath, parted_name)
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(start_time),
                    "-i", path, "-fs", str(split_size), "-map_chapters", "-1", "-async", "1",
                    "-strict", "-2","-c", "copy", out_path]
            if not noMap:
                cmd.insert(10, '-map')
                cmd.insert(11, '0')
            if listener == 'cancelled' or listener is not None and listener.returncode == -9:
                return False, None
            listener = await asyncio.create_subprocess_exec(*cmd, stderr=asyncio.subprocess.PIPE)
            code = await listener.wait()
            if code == -9:
                return False, None
            elif code != 0:
                err = (await listener.stderr.read()).decode().strip()
                try:
                    os.remove(out_path)
                except:
                    pass
                if not noMap:
                    logging.warning(
                        f"{err}. Retrying without map, -map 0 not working in all situations. Path: {path}")
                    return await split_large_files(path, size, file_, dirpath, split_size, listener, start_time, i, True, True)
                else:
                    logging.warning(
                        f"{err}. Unable to split this video, if it's size less than {SPLIT_SIZE} will be uploaded as it is. Path: {path}")
                return False, None
            out_size = os.path.getsize(out_path)
            if out_size > SPLIT_SIZE:
                dif = out_size - SPLIT_SIZE
                split_size -= dif + 5000000
                os.remove(out_path)
                return await split_large_files(path, size, file_, dirpath, split_size, listener, start_time, i, True, noMap)
            lpd = (await findVideoMetadata(path))[2]
            if lpd == 0:
                logging.error(
                    f'Something went wrong while splitting, mostly file is corrupted. Path: {path}')
                break
            elif duration == lpd:
                if not noMap:
                    logging.warning(f"Retrying without map. -map 0 not working in all situations. Path: {path}")
                    try:
                        os.remove(out_path)
                    except:
                        pass
                    return split_large_files(path, size, file_, dirpath, split_size, listener, start_time, i, True, True)
                else:
                    logging.warning(f"This file has been splitted with default stream and audio, so you will only see one part with less size from orginal one because it doesn't have all streams and audios. This happens mostly with MKV videos. noMap={noMap}. Path: {path}")
                    break
            elif lpd <= 3:
                os.remove(out_path)
                break
            start_time += lpd - 5
            i += 1
    else:
        out_path = os.path.join(dirpath, f"{file_}.")
        listener = await asyncio.create_subprocess_exec("split", "--numeric-suffixes=1", "--suffix-length=3",
                                                       f"--bytes={split_size}", path, out_path, stderr=asyncio.subprocess.PIPE)
        code = await listener.wait()
        if code == -9:
            return False, None
        elif code != 0:
            err = (await listener.stderr.read()).decode().strip()
            logging.error(err)
    return True, dirpath


async def cult_small_video(video_file, out_put_file_name, start_time, end_time):
    file_genertor_command = [
        "ffmpeg",
        "-hide_banner",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-fs",
        str(SPLIT_SIZE),
        "-async",
        "1",
        "-strict",
        "-2",
        "-c",
        "copy",
        out_put_file_name,
    ]

    t_response, e_response = await run_comman_d(file_genertor_command)
    logging.info(t_response)
    return out_put_file_name


async def run_comman_d(command_list):
    process = await asyncio.create_subprocess_exec(
        *command_list,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return t_response, e_response


def extract_file_name(msg: Message):
    def get_file_ext():
        ext = None
        if msg.media == MessageMediaType.DOCUMENT:
            ext = ".zip"
        elif msg.media == MessageMediaType.VIDEO:
            ext = ".mp4"
        elif msg.media == MessageMediaType.AUDIO:
            ext = ".mp3"
        elif msg.media == MessageMediaType.VOICE:
            ext = ".ogg"
        elif msg.media == MessageMediaType.PHOTO:
            ext = ".jpg"
        else:
            ext = ".mp4"
        return ext
    media = msg.document or msg.video or msg.audio or msg.voice or msg.photo or msg.animation or msg.sticker or msg.video_note
    if media:
        file_name = getattr(media, "file_name", str(uuid.uuid4().hex) + (get_file_ext() or ".mp4"))
        return file_name

# download ---------------------------------------------------------------------------------------------------------------

async def download(client:CustomBot, msg, editable_msg, file_name=None):
    if not file_name:
        file_name = extract_file_name(msg) or str(uuid.uuid4().hex) + ".mp4"
    if file_name:
        file_name = os.path.basename(file_name).replace(os.sep, "-")
    file = None
    try:
        dl_dir = os.path.join(DL_DIR, str(client.me.id), file_name)
        file = await client.download_media(
                msg,
                file_name=dl_dir,
                progress=progress_for_pyrogram,
                progress_args=(
                    client,
                    "**🔻 DOWNLOADING:**\n",
                    editable_msg,
                    time.time()
                )
            )
        return True, file
    except FileNotFoundError:
        if file:
            delete_file(file)
        return await download(client, msg, editable_msg, file_name=file_name)
    except (ChannelInvalid, ChatInvalid, ChatIdInvalid, PeerIdInvalid):
        return False, "⚠️ Invalid link, check your link and try again."
    except ChannelBanned:
        return False, "⚠️ You are banned from this chat"
    except ChannelPrivate:
        return False, "⚠️ You are not joined in this channel"
    except UserNotParticipant:
        return False, "⚠️ You are not joined in this channel"
    except Exception as e:
        if "This message doesn't contain any downloadable" in str(e):
            return False, "⚠️ This message doesn't contain any downloadable media."
        else:
            return False, str(e)

# upload ---------------------------------------------------------------------------------------------------------------
  
async def upload(client:CustomBot, file, to, msg, editable_msg, thumb_path=None, caption=None):

    if not client.me.is_premium and os.path.getsize(file) > SPLIT_SIZE:
        try:
            await editable_msg.edit("🔺 Splitting the file...")
        except:
            pass
        ikOk, dirpath = await split_large_files(file, size=os.path.getsize(file), file_=os.path.basename(file))
        if not ikOk:
            return False, "⚠️ Unable to split the file, try again later."
        for file in os.listdir(dirpath):
            file_path = os.path.join(dirpath, file)
            if not os.path.isfile(file_path):
                continue
            try:
                sent = await upload(client, file_path, to, msg, editable_msg, thumb_path=thumb_path, caption=caption)
            except Exception as e:
                logging.exception(e)
                return False, str(e)
            return True, sent

    try:
        if msg.media==MessageMediaType.VIDEO_NOTE:
            height, width, duration = await findVideoMetadata(file)
            print(f'd: {duration}, w: {width}, h:{height}')
            try:
                if not thumb_path:
                    thumb_path = await screenshot(file, duration)
            except Exception:
                thumb_path = None
            sent = await client.send_video_note(
                chat_id=to,
                video_note=file,
                length=height, duration=duration, 
                thumb=thumb_path,
                progress=progress_for_pyrogram,
                progress_args=(
                    client,
                    '**🔺 UPLOADING:**\n',
                    editable_msg,
                    time.time()
                )
            )
        elif msg.media==MessageMediaType.VIDEO:
            height, width, duration = await findVideoMetadata(file)
            print(f'd: {duration}, w: {width}, h:{height}')
            try:
                if not thumb_path:
                    thumb_path = await screenshot(file, duration)
            except Exception:
                thumb_path = None
            sent = await client.send_video(
                chat_id=to,
                video=file,
                caption=caption,
                supports_streaming=True,
                height=height, width=width, duration=duration, 
                thumb=thumb_path,
                mime_type=msg.video.mime_type,
                progress=progress_for_pyrogram,
                progress_args=(
                    client,
                    '**🔺 UPLOADING:**\n',
                    editable_msg,
                    time.time()
                )
            )
        elif msg.media==MessageMediaType.VOICE:
            sent = await client.send_voice(to, file, caption=caption)
        elif msg.media==MessageMediaType.PHOTO:
            try:
                await editable_msg.edit("🔺 Uploading photo...")
            except:
                pass
            sent = await client.send_photo(to, file, caption=caption)
        else:
            sent = await client.send_document(
                to,
                file, 
                caption=caption,
                thumb=thumb_path,
                progress=progress_for_pyrogram,
                progress_args=(
                    client,
                    '**🔺 UPLOADING:**\n',
                    editable_msg,
                    time.time()
                )
            )
        delete_file(file)
        if thumb_path:
            delete_file(thumb_path)
        try:
            await editable_msg.edit("Finalizing the upload...")
        except:
            pass
        return True, sent
    except (MessageNotModified, FloodPremiumWait, FloodWait):
        # If the message is not modified, it means the upload was successful but no changes were made to the message.
        return True, None
    except (ChannelInvalid, ChatInvalid) as e:
        logging.exception(e)
        False, "⚠️ You are not joined this channel/chat with the logged in account"
    except (ChatIdInvalid, PeerIdInvalid) as e:
        logging.exception(e)
        return False, "⚠️ Check your setchat ID or add bot as admin in your setchat channel."
    except Exception as e:
        logging.exception(e)
        if "'NoneType' object has no attribute 'name'" in str(e):
            return True, None
        if "size equals" in str(e):
            await asyncio.sleep(60)
            try:
                os.remove(file)
            except:
                pass
            return False, None
        elif "messages.SendMedia" in str(e) \
        or "SaveBigFilePartRequest" in str(e) \
        or "SendMediaRequest" in str(e):
            try:
                sent = await client.send_document(
                    to,
                    file, 
                    caption=caption,
                    thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        '**🔺 UPLOADING:**\n',
                        editable_msg,
                        time.time()
                    )
                )
                delete_file(file)
                if thumb_path:
                    delete_file(thumb_path)
                return True, sent
            except Exception as e:
                return False, str(e)
        return False, str(e)
    return False, None
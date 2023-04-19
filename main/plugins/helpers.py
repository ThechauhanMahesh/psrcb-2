#Github.com/Vasusen-code

from .. import MONGODB_URI, bot
from .. import FORCESUB as FSUB

from main.Database.database import Database

from pyrogram import Client
from pyrogram.errors import FloodWait, InviteHashInvalid, InviteHashExpired, UserAlreadyParticipant, BadRequest

from decouple import config
from pathlib import Path
from datetime import datetime as dt
import asyncio, subprocess, re, os, time

from telethon import errors, events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

#Forcesub-----------------------------------------------------------------------------------

async def force_sub(id):
    try:
        x = await bot(GetParticipantRequest(channel=FSUB, participant=int(id)))
        left = x.stringify()
        if 'left' in left:
            ok = True
        else:
            ok = False
    except UserNotParticipantError:
        ok = True 
    return ok   

#Multi client-------------------------------------------------------------------------------------------------------------

async def login(sender, i, h, s):
    db = Database(MONGODB_URI, 'saverestricted')
    await db.update_api_id(sender, i)
    await db.update_api_hash(sender, h)
    await db.update_session(sender, s)
    
async def logout(sender):
    db = Database(MONGODB_URI, 'saverestricted')
    await db.rem_api_id(sender)
    await db.rem_api_hash(sender)
    await db.rem_session(sender)
   
#Join private chat-------------------------------------------------------------------------------------------------------------

async def join(client, invite_link):
    try:
        await client.join_chat(invite_link)
        return "Successfully joined the Channel"
    except UserAlreadyParticipant:
        return "User is already a participant."
    except (InviteHashInvalid, InviteHashExpired):
        return "Could not join. Maybe your link is expired or Invalid."
    except FloodWait:
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
        link = [x[0] for x in url][0]
        if link:
            return link
        else:
            return False
    except Exception:
        return False
    
#Anti-Spam---------------------------------------------------------------------------------------------------------------

#Set timer to avoid spam
async def set_timer(bot, sender, list1, list2, t):
    now = time.time()
    list2.append(f'{now}')
    list1.append(f'{sender}')
    await bot.send_message(sender, f'You can start a new process again after {t} seconds.')
    await asyncio.sleep(int(t))
    list2.pop(int(list2.index(f'{now}')))
    list1.pop(int(list1.index(f'{sender}')))
    
#check time left in timer
def check_timer(sender, list1, list2, t):
    if f'{sender}' in list1:
        index = list1.index(f'{sender}')
        last = list2[int(index)]
        present = time.time()
        return False, f"You have to wait {int(t)-round(present-float(last))} seconds more to start a new process!"
    else:
        return True, None

#Screenshot---------------------------------------------------------------------------------------------------------------

def hhmmss(seconds):
    x = time.strftime('%H:%M:%S',time.gmtime(seconds))
    return x

async def screenshot(video, duration, sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    time_stamp = hhmmss(int(duration)/2)
    out = f'{sender}-' + dt.now().isoformat("_", "seconds") + ".jpg"
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
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    x = stderr.decode().strip()
    y = stdout.decode().strip()
    if os.path.isfile(out):
        return out
    else:
        None       

#pyUltroid -------------

import json
from telethon.tl.types import DocumentAttributeAudio

async def bash(cmd, run_code=0):
    """
    run any command in subprocess and get output or error."""
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip() or None
    out = stdout.decode().strip()
    if not run_code and err:
        split = cmd.split()[0]
        if f"{split}: not found" in err:
            return out, f"{split.upper()}_NOT_FOUND"
    return out, err

async def metadata(file):
    out, _ = await bash(f'mediainfo "{_unquote_text(file)}" --Output=JSON')
    if _ and _.endswith("NOT_FOUND"):
        return _
    data = {}
    _info = json.loads(out)["media"]["track"]
    info = _info[0]
    if info.get("Format") in ["GIF", "PNG"]:
        return {
            "height": _info[1]["Height"],
            "width": _info[1]["Width"],
            "bitrate": _info[1].get("BitRate", 320),
        }
    if info.get("VideoCount"):
        data["height"] = int(float(_info[1].get("Height", 720)))
        data["width"] = int(float(_info[1].get("Width", 1280)))
        data["bitrate"] = int(_info[1].get("BitRate", 320))
    data["duration"] = int(float(info.get("Duration", 0)))
    return data


async def set_attributes(file):
    data = await metadata(file)
    if not data:
        return None
    if "width" in data:
        return [
            DocumentAttributeVideo(
                duration=data.get("duration", 0),
                w=data.get("width", 512),
                h=data.get("height", 512),
                supports_streaming=True,
            )
        ]
   

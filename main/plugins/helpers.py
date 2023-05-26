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

#Subscription-------------------------------------------------------------------------------------------------------------

from datetime import timedelta
from datetime import date

async def check_subsciption(id):
    pass

async def set_subscription(user_id, dos, days, plan):
    if not dos:
        today = date.today()
    else:
        today = dos
    expiry_date = today + timedelta(days=days)
    data = {"dos":today, "doe":expiry_date, "plan":plan}
    db = Database(MONGODB_URI, 'PremiumSRCB')
    await db.update_data(data)
    
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
    db = Database(MONGODB_URI, 'PremiumSRCB')
    await db.update_api_id(sender, i)
    await db.update_api_hash(sender, h)
    await db.update_session(sender, s)
    
async def logout(sender):
    db = Database(MONGODB_URI, 'PremiumSRCB')
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
async def set_timer(bot, sender, t):
    db = Database(MONGODB_URI, 'PremiumSRCB')
    await db.update_process(sender)
    await bot.send_message(sender, f'You can start a new process again after {t} seconds.')
    await asyncio.sleep(int(t))
    await db.rem_process(sender)
    
# #check time left in timer
# async def check_timer(sender):
#     db = Database(MONGODB_URI, 'PremiumSRCB')
#     process = (await db.get_process(sender))["process"]
#     if process == True:
#         return False
#     else:
#         return True
    
# async def rem_timer(sender):
#     db = Database(MONGODB_URI, 'PremiumSRCB')
#     await db.rem_process(sender)

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

import subprocess
import shlex
import json

# function to find the resolution of the input video file
def findVideoResolution(pathToInputVideo):
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

    return int(height), int(width), int(duration_seconds)

def duration(pathToInputVideo):
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", pathToInputVideo])
    ffprobe_data = json.loads(out)
    duration_seconds = float(ffprobe_data["format"]["duration"])
    return int(duration_seconds)

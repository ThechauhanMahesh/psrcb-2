import io
import sys
import traceback
from os import remove

from .. import bot as CA
from .. import AUTH
from ethon.pyfunc import bash
from telethon import *

async def aexec(code, event):
    exec(
        (
            (
                ("async def __aexec(e, client): " + "\n message = event = e")
                + "\n reply = await event.get_reply_message()"
            )
            + "\n chat = event.chat_id"
        )
        + "".join(f"\n {l}" for l in code.split("\n"))
    )

    return await locals()["__aexec"](event, event.client)

 
@CA.on(events.NewMessage(incoming=True, pattern="!bash"))
async def bash_command(event):
    if not f'{event.sender_id}' in AUTH:
        return
    xx = await event.reply('Running.')
    try:
        cmd = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await event.reply("Insufficient code len.")
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    stdout, stderr = bash(cmd)
    OUT = f"**☞ BASH\n\n• COMMAND:**\n`{cmd}` \n\n"
    if stderr:
        OUT += f"**• ERROR:** \n`{stderr}`\n\n"
    if stdout:
        _o = stdout.split("\n")
        o = "\n".join(_o)
        OUT += f"**• OUTPUT:**\n`{o}`"
    if not stderr and not stdout:
        OUT += "**• OUTPUT:**\n`Success`"      
    if len(OUT) > 4096:
        text = OUT.replace("`", "").replace("**", "").replace("__", "")
        with io.BytesIO(str.encode(text)) as out_file:
            out_file.name = "bash.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=f"`{cmd}`" if len(cmd) < 998 else None,
                reply_to=reply_to_id,
            )

            await xx.delete()
    else:
        await xx.edit(OUT)   

@CA.on(events.NewMessage(incoming=True, from_users=AUTH , pattern="!eval"))        
async def eval(event):
    if len(event.text) > 5 and event.text[5] != " ":
        return await event.reply("insufficient code len.")
    xx = await event.reply('Running.')
    try:
        cmd = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await event.reply("IndrxError!")
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    reply_to_id = event.message.id
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "success"
    final_output = (
        "__►__ **EVALPy**\n```{}``` \n\n __►__ **OUTPUT**: \n```{}``` \n".format(
            cmd,
            evaluation,
        )
    )  
    if len(final_output) > 4096:
        text = final_output.replace("`", "").replace("**", "").replace("__", "")
        with io.BytesIO(str.encode(text)) as out_file:
            out_file.name = "eval.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=f"```{cmd}```" if len(cmd) < 998 else None,
                reply_to=reply_to_id,
            )
            await xx.delete()
    else:
        await xx.edit(final_output)


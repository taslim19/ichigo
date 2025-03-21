__MODULE__ = "Misc"
__HELP__ = """
Misc Help

• Command: <code>{0}logger</code> [on/off]
• Explanation: To find out if there are incoming messages from other users, or when you are tagged by others.

- <code>{0}logger on</code> -> To turn on the log group.
- <code>{0}logger off</code> -> To turn off the log group.

• Command: <code>{0}addsudo</code> [reply/username/id]
• Explanation: Add a sudo user.

• Command: <code>{0}delsudo</code> [reply/username/id]
• Explanation: Delete a sudo user.

• Command: <code>{0}sudolist</code>
• Explanation: Check sudo users.
"""


import asyncio

from pyrogram.enums import *
from pyrogram.errors import FloodWait
from pyrogram.types import *

from ubot import *


@PY.GC()
async def _(client, message):
    log = await get_log(client)
    cek = await get_log_group(client.me.id)
    if not cek:
        return
    user = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
    message_link = message.link
    text = f"""
📨 <b>TAGS MESSAGE</b>
• <b>Logs:</b> <code>{client.me.first_name}</code>
• <b>Group:</b> <code>{message.chat.title}</code>
• <b>From:</b> <code>{user}</code>
• <b>Message:</b> <code>{message.text}</code>

• <b>Group Link:</b> [Here]({message_link})
"""
    try:
        await client.send_message(
            log.id,
            text,
            disable_web_page_preview=True,
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await client.send_message(
            log.id,
            text,
            disable_web_page_preview=True,
        )


@PY.PC()
async def _(client, message):
    log = await get_log(client)
    cek = await get_log_group(client.me.id)
    if not cek:
        return
    if message.chat.id == 777000:
        return
    async for x in client.search_messages(message.chat.id, limit=1):
        await x.forward(log.id)


@PY.UBOT("logger", sudo=True)
async def _(client, message):
    xx = await message.reply(f"**Processing...**")
    cek = get_arg(message)
    logs = await get_log_group(client.me.id)
    if cek.lower() == "on":
        if not logs:
            await set_log_group(client.me.id, logger=True)
            await create_botlog(client)
            ajg = await get_log(client)
            babi = await client.export_chat_invite_link(int(ajg.id))
            return await xx.edit(f" Log Group Successfully Activated:\n\n{babi}")
        else:
            return await xx.edit(f" Your Log Group is Already Active.")
    if cek.lower() == "off":
        if logs:
            await del_log_group(client.me.id)
            ajg = await get_log(client)
            await client.delete_supergroup(int(ajg.id))
            return await xx.edit(f" Log Group Successfully Deactivated.")
        else:
            return await xx.edit(f" Your Log Group is Already Deactivated.")
    else:
        return await xx.edit(
            f"Invalid format. Please use <code>{message.text} on/off</code>"
        )


@PY.UBOT("addsudo", sudo=True)
async def _(client, message):
    msg = await message.reply(f"<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>Please reply to user message/username/user id</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await ambil_list_var(client.me.id, "SUDO_USER", "ID_NYA")

    if user.id in sudo_users:
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) is already a sudo user.</b>"
        )

    try:
        await add_var(client.me.id, "SUDO_USER", user.id, "ID_NYA")
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) has been added as a sudo user.</b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("delsudo", sudo=True)
async def _(client, message):
    msg = await message.reply(f"<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>Please reply to user message/username/user id.</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await ambil_list_var(client.me.id, "SUDO_USER", "ID_NYA")

    if user.id not in sudo_users:
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) is not a sudo user.</b>"
        )

    try:
        await rem_var(client.me.id, "SUDO_USER", user.id, "ID_NYA")
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) has been removed from sudo users.</b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("sudolist", sudo=True)
async def _(client, message):
    msg = await message.reply(f"<b>Processing...</b>")
    sudo_users = await ambil_list_var(client.me.id, "SUDO_USER", "ID_NYA")

    if not sudo_users:
        return await msg.edit(f"<b>No sudo users found.</b>")

    sudo_list = []
    for user_id in sudo_users:
        try:
            user = await client.get_users(int(user_id))
            sudo_list.append(
                f" • [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code>"
            )
        except:
            continue

    if sudo_list:
        response = (
            f"<b>User List:</b>\n"
            + "\n".join(sudo_list)
            + f"\n<b> • </b> <code>{len(sudo_list)}</code>"
        )
        return await msg.edit(response)
    else:
        return await msg.edit("<b>Error</b>")

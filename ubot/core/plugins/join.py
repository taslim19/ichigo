from pyrogram import enums

from ubot import *


async def join(client, message):
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply("Processing...")
    try:
        await xxnx.edit(f"Successfully joined : `{Man}`")
        await client.join_chat(Man)
    except Exception as ex:
        await xxnx.edit(f"ERROR: \n\n{str(ex)}")


async def leave(client, message):
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply("Processing...")
    if message.chat.id in BLACKLIST_CHAT:
        return await xxnx.edit("You are not allowed to use this command here.")
    try:
        await xxnx.edit_text(f"{client.me.first_name} I'm sed .")
        await client.leave_chat(Man)
    except Exception as ex:
        await xxnx.edit_text(f"ERROR: \n\n{str(ex)}")


async def kickmeall(client, message):
    Man = await message.reply("Global Group Exit Process...")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(f"Successfully left {done} groups, failed to leave {er} groups.")


async def kickmeallch(client, message):
    Man = await message.reply("Global Channel Exit Process...")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.CHANNEL):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(
        f""Successfully left {done} channels, failed to leave {er} channels."
    )

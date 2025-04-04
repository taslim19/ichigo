from pyrogram import *
from pyrogram.types import *

from ubot import *

PM_GUARD_WARNS_DB = {}
PM_GUARD_MSGS_DB = {}

flood = {}
flood2 = {}

DEFAULT_TEXT = """
<b>I am {} who guards this Chat Room. Don't spam or you will be automatically blocked.</b>
"""

PM_WARN = """
<b>PM Security Of {} !!</b>

<b>{}</b>

<b>Warning `{}` of `{}` !!</b>
"""

LIMIT = 5


async def permitpm(client, message):
    user_id = client.me.id
    babi = await message.reply("`Processing...`")
    bacot = get_arg(message)
    if not bacot:
        return await babi.edit(f"`Use Format: `{0}pmpermit on or off`.`")
    is_already = await get_var(user_id, "ENABLE_PM_GUARD")
    if bacot.lower() == "on":
        if is_already:
            return await babi.edit("`PMPermit is already enabled.`")
        await set_var(user_id, "ENABLE_PM_GUARD", True)
        await babi.edit("`PMPermit has been enabled.`")
    elif bacot.lower() == "off":
        if not is_already:
            return await babi.edit("`PMPermit is already disabled.`")
        await set_var(user_id, "ENABLE_PM_GUARD", False)
        await babi.edit("`PMPermit has been disabled.`")
    else:
        await babi.edit(f"`Use Format: `{0}pmpermit on or off`.`")


async def approve(client, message):
    babi = await message.reply("`Processing...`")
    chat_type = message.chat.type
    client.me.id
    if chat_type == "me":
        return await babi.edit("`Are you crazy?`")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not message.reply_to_message:
            return await babi.edit("`Reply to user's message to approve.`")
        user_id = message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
    else:
        return
    already_apprvd = await check_user_approved(user_id)
    if already_apprvd:
        return await babi.edit("**This user is already approved.**")
    if user_id in PM_GUARD_WARNS_DB:
        PM_GUARD_WARNS_DB.pop(user_id)
        try:
            await client.delete_messages(
                chat_id=user_id, message_ids=PM_GUARD_MSGS_DB[user_id]
            )
        except BaseException:
            pass
    await add_approved_user(user_id)
    await babi.edit("**Alright, this user is approved to send messages.**")


async def disapprove(client, message):
    babi = await message.reply("`Processing...`")
    client.me.id
    chat_type = message.chat.type
    if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not message.reply_to_message.from_user:
            return await babi.edit("`Reply to user's message to disapprove.`")
        user_id = message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
    else:
        return
    already_apprvd = await check_user_approved(user_id)
    if not already_apprvd:
        return await babi.edit(
            "**This user is not approved to send messages yet.**"
        )
    await rm_approved_user(user_id)
    await babi.edit("**Alright, this user is disapproved from sending messages.**")


async def set_msg(client, message):
    babi = await message.reply("`Processing...`")
    user_id = client.me.id
    r_msg = message.reply_to_message
    args_txt = get_arg(message)
    if r_msg:
        if r_msg.text:
            pm_txt = r_msg.text
        else:
            return await babi.edit(
                "`Please reply to a message to set it as PMPermit text!`"
            )
    elif args_txt:
        pm_txt = args_txt
    else:
        return await babi.edit(
            "`Please reply to a message or provide text to set as PMPermit text!\n`Example: `{0}setmsg Hello, I am anuan`"
        )
    await set_var(user_id, "CUSTOM_PM_TEXT", pm_txt)
    await babi.edit(f"`PMPermit message has been set to: `{pm_txt}`.`")


async def set_limit(client, message):
    babi = await message.reply("`Processing...`")
    user_id = client.me.id
    args_txt = get_arg(message)
    if args_txt:
        if args_txt.isnumeric():
            pm_warns = int(args_txt)
        else:
            return await babi.edit("`Please provide a number for the limit!`")
    else:
        return await babi.edit(
            f"`Please provide a number for the limit!\n`Example: `{0}setlimit 5`"
        )
    await set_var(user_id, "CUSTOM_PM_WARNS_LIMIT", pm_warns)
    await babi.edit(f"`Limit has been set to: `{args_txt}`.`")


async def handle_pmpermit(client, message):
    user_id = client.me.id
    siapa = message.from_user.id
    biji = message.from_user.mention
    chat_id = message.chat.id
    in_user = message.from_user
    fsdj = await check_user_approved(chat_id)
    is_pm_guard_enabled = await get_var(user_id, "ENABLE_PM_GUARD")
    if not is_pm_guard_enabled:
        return

    if fsdj:
        return

    if in_user.is_fake or in_user.is_scam:
        await message.reply("**You seem suspicious...**")
        return await client.block_user(in_user.id)
    if in_user.is_support or in_user.is_verified or in_user.is_self:
        return
    if siapa in DEVS:
        try:
            await add_approved_user(chat_id)
            await client.send_message(
                chat_id,
                f"<b>Accepting message from {biji} !!\nDetected as Founder of {bot.me.first_name}.</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except BaseException:
            pass
        return
    if siapa in await get_seles():
        try:
            await add_approved_user(chat_id)
            await client.send_message(
                chat_id,
                f"<b>Accepting message from {biji} !!\nDetected as Admin of {bot.me.first_name}.</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except BaseException:
            pass
        return

    master = await client.get_me()
    getc_pm_txt = await get_var(user_id, "CUSTOM_PM_TEXT")
    getc_pm_warns = await get_var(user_id, "CUSTOM_PM_WARNS_LIMIT")
    custom_pm_txt = getc_pm_txt if getc_pm_txt else DEFAULT_TEXT
    custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT
    if in_user.id in PM_GUARD_WARNS_DB:
        try:
            if message.chat.id in PM_GUARD_MSGS_DB:
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=PM_GUARD_MSGS_DB[message.chat.id],
                )
        except BaseException:
            pass
        PM_GUARD_WARNS_DB[in_user.id] += 1
        if PM_GUARD_WARNS_DB[in_user.id] >= custom_pm_warns:
            await message.reply(
                f"`I have given {custom_pm_warns} warnings\nWait for my master to approve your message, or you will be blocked!`"
            )
            return await client.block_user(in_user.id)
        else:
            rplied_msg = await message.reply(
                PM_WARN.format(
                    master.first_name,
                    custom_pm_txt.format(bot.me.first_name),
                    PM_GUARD_WARNS_DB[in_user.id],
                    custom_pm_warns,
                )
            )
    else:
        PM_GUARD_WARNS_DB[in_user.id] = 1
        rplied_msg = await message.reply(
            PM_WARN.format(
                master.first_name,
                custom_pm_txt.format(bot.me.first_name),
                PM_GUARD_WARNS_DB[in_user.id],
                custom_pm_warns,
            )
        )
    PM_GUARD_MSGS_DB[message.chat.id] = rplied_msg.id

import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *

from ubot import *

BANNED_USERS = filters.user()


async def admin_bannen(client, message):
    if message.command[0] == "kick":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text("user not found.")
        if user_id == (await client.get_me()).id:
            return await message.reply_text("cannot kick yourself.")
        if user_id == OWNER_ID:
            return await message.reply_text("he/she is the owner of your bot.")
        if user_id in (await list_admins(message)):
            return await message.reply_text("Cannot kick an admin.")
        mention = (await client.get_users(user_id)).mention
        await message.reply_to_message.delete()
        msg = f"<b>Kicked User :</b> {mention}\n<b>Admin :</b> {message.from_user.mention}"
        if reason:
            msg += f"\n<b>Reason :</b> {reason}"
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg)
            await asyncio.sleep(1)
            await message.chat.unban_member(user_id)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "ban":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text("user not found .")
        if user_id == (await client.get_me()).id:
            return await message.reply_text("cannot kick yourself.")
        if user_id == OWNER_ID:
            return await message.reply_text("he/she is the owner of your bot.")
        if user_id in (await list_admins(message)):
            return await message.reply_text("Cannot kick an admin.")
        try:
            mention = (await client.get_users(user_id)).mention
        except IndexError:
            mention = (
                message.reply_to_message.sender_chat.title
                if message.reply_to_message
                else "Anon"
            )
        await message.reply_to_message.delete()
        msg = f"<b>Banned Users :</b> {mention}\n<b>Admin :</b> {message.from_user.mention}"
        if reason:
            msg += f"\n<b>Reason :</b> {reason}"
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "mute":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text("user not found .")
        if user_id == (await client.get_me()).id:
            return await message.reply_text("Cannot mute yourself.")
        if user_id == OWNER_ID:
            return await message.reply_text("He/She is the owner of your bot.")
        if user_id in (await list_admins(message)):
            return await message.reply_text("Cannot mute a fellow admin.")
        mention = (await client.get_users(user_id)).mention
        await message.reply_to_message.delete()
        msg = f"<b>Muted Users :</b> {mention}\n<b>Admin :</b> {message.from_user.mention}"
        if reason:
            msg += f"\n<b>Reason :</b> {reason}"
        try:
            await message.chat.restrict_member(user_id, ChatPermissions())
            await message.reply(msg)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unmute":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text("user not found.")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"<b>{mention} no longer muted.</b>")
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unban":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text("Cannot find the user")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"<b>{mention} Able to join now .</b>")
        except Exception as error:
            await message.reply(error)


async def global_banned(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("<code>Processing....</code>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            "Gunakan format: <code>gban</code> [user_id/username/reply to the user]"
        )
    elif len(cmd) == 1:
        message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await Tm.edit("Cannot find that user.")
        return
    iso = 0
    gagal = 0
    prik = user.id
    prok = await get_seles()
    gua = client.me.id
    udah = await is_banned_user(gua, prik)
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id

            if prik in DEVS:
                return await Tm.edit(
                    "You cannot globally ban him/her because they are my creator."
                )
            elif prik in prok:
                return await Tm.edit(
                    "You cannot globally ban him/her because they are an Admin of your Userbot."
                )
            elif udah:
                return await Tm.edit("This user has already been globally banned.")
            elif prik not in prok and prik not in DEVS:
                try:
                    BANNED_USERS.add(prik)
                    await add_banned_user(gua, prik)
                    await client.ban_chat_member(chat, prik)
                    iso = iso + 1
                    await asyncio.sleep(0.1)
                except BaseException:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)
    return await Tm.edit(
        f"""
<b>Global Banned</b>

<b>Successfully Banned: {iso} Chat</b>
<b>failed to ban: {gagal} Chat</b>
<b>User: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
"""
    )


async def cung_ban(client, message):
    user_id = await extract_user(message)
    if message.from_user.id != client.me.id:
        Tm = await message.reply("<code>Processing....</code>")
    else:
        Tm = await message.reply("<code>Processing....</code>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            "use format: <code>ungban</code> [user_id/username/reply to user]"
        )
    elif len(cmd) == 1:
        message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await Tm.edit("Could not find that user")
        return
    iso = 0
    gagal = 0
    prik = user.id
    gua = client.me.id
    await is_banned_user(gua, prik)
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id
            if prik in BANNED_USERS:
                BANNED_USERS.remove(prik)
            try:
                await remove_banned_user(gua, prik)
                await client.unban_chat_member(chat, prik)
                iso = iso + 1
                await asyncio.sleep(0.1)
            except BaseException:
                gagal = gagal + 1
                await asyncio.sleep(0.1)

    return await Tm.edit(
        f"""
<b>Global Unbanned</b>

<b>Successful Unbanned: {iso} Chat</b>
<b>Failed UnBanned: {gagal} Chat</b>
<b>User: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
"""
    )


async def gbanlist(client, message):
    gua = client.me.id
    total = await get_banned_count(gua)
    if total == 0:
        return await message.reply("No users have been globally banned yet.")
    nyet = await message.reply("`Processing...`")
    msg = "**Total Gbanned:** \n\n"
    tl = 0
    org = await get_banned_users(gua)
    for i in org:
        tl += 1
        try:
            user = await client.get_users(i)
            user = user.first_name if not user.mention else user.mention
            msg += f"{tl}• {user}\n"
        except Exception:
            msg += f"{tl}• {i}\n"
            continue
    if tl == 0:
        return await nyet.edit("No users have been banned yet.")
    else:
        return await nyet.edit(msg)


async def pin_message(client, message):
    mmk = await message.reply("<code>Processing...</code>")
    if not message.reply_to_message:
        return await mmk.edit("Reply to the message to pin/unpin .")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await mmk.edit(
            f"<code>Unpinned [this]({r.link}) message.</code>",
            disable_web_page_preview=True,
        )
    try:
        await r.pin(disable_notification=True)
        await mmk.edit(
            f"<code>Pinned [this]({r.link}) message.</code>",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        return await mmk.edit("<b> You are not an admin in this group!</b>")


async def promotte(client, message):
    user_id = await extract_user(message)
    biji = await message.reply("<code>Processing...</code>")
    if not user_id:
        return await biji.edit("user not found.")
    (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    try:
        if message.command[0][0] == "f":
            await message.chat.promote_member(
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                ),
            )
            await asyncio.sleep(1)

            umention = (await client.get_users(user_id)).mention
            return await biji.edit(f"Full Promoted! {umention}")

        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False,
            ),
        )
        await asyncio.sleep(1)

        umention = (await client.get_users(user_id)).mention
        await biji.edit(f"Promoted! {umention}")
    except ChatAdminRequired:
        return await biji.edit("<b>You are not an admin in this group.!</b>")


async def demote(client, message):
    user_id = await extract_user(message)
    sempak = await message.reply("<code>Processing...</code>")
    if not user_id:
        return await sempak.edit("user not found ")
    if user_id == client.me.id:
        return await sempak.edit("cannot demote yourself.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    await asyncio.sleep(1)

    umention = (await client.get_users(user_id)).mention
    await sempak.edit(f"Demoted! {umention}")


async def invite_link(client, message):
    um = await message.reply("`Processing...`")
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await um.edit_text(f"**Link Invite:** {link}")
        except ChatAdminRequired:
            return await biji.edit("<b>you are not an admin in this group!</b>")

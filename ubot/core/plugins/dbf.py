from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from ubot import *

# ========================== #
# 𝔻𝔸𝕋𝔸𝔹𝔸𝕊𝔼 ℙℝ𝔼𝕄𝕀𝕌𝕄 #
# ========================== #


async def prem_user(client, message):
    if message.from_user.id not in await get_seles():
        return
    user_id, get_bulan = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply(f"<b>{message.text} [user_id/username - months]</b>")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_bulan:
        get_bulan = 1
    premium = await get_prem()
    if get_id in premium:
        return await message.reply(f"User with ID: `{get_id}` already has access!")
    added = await add_prem(get_id)
    if added:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        expired_formatted = expired.strftime("%d %b %Y")
        await set_expired_date(get_id, expired)
        await message.reply(
            f"✅ {get_id} Successfully activated for `{get_bulan}` months\n\nExpires on: `{expired_formatted}`."
        )
        await bot.send_message(
            get_id,
            f"Congratulations! Your account now has access to create userbots\nExpires on: {expired_formatted}.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Continue Userbot Creation", callback_data="bahan"
                        )
                    ],
                ]
            ),
        )
        await bot.send_message(
            OWNER_ID,
            f"• {message.from_user.id} ─> {get_id} •",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👤 Profile",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "Profile 👤", callback_data=f"profil {get_id}"
                        ),
                    ],
                ]
            ),
        )
    else:
        await Tm.delete()
        await message.reply_text("Error")


async def unprem_user(client, message):
    user_id = await extract_user(message)
    if message.from_user.id not in await get_seles():
        return
    if not user_id:
        return await message.reply("Reply to user's message or provide user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    delpremium = await get_prem()
    if user.id not in delpremium:
        return await message.reply("Not found")
    removed = await remove_prem(user.id)
    if removed:
        await message.reply(f" ✅ {user.mention} successfully removed")
    else:
        await Tm.delete()
        await message.reply_text("An unknown error occurred")


async def get_prem_user(client, message):
    text = ""
    count = 0
    if message.from_user.id not in KYNAN:
        return
    for user_id in await get_prem():
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        await message.reply_text("No users found")
    else:
        await message.reply_text(text)


# ========================== #
# DATABASE BLACKLIST #
# ========================== #


async def add_blaclist(client, message):
    Tm = await message.reply("Please wait...")
    chat_id = message.chat.id
    blacklist = await get_chat(client.me.id)
    if chat_id in blacklist:
        return await message.reply("This group is already in the blacklist")
    add_blacklist = await add_chat(client.me.id, chat_id)
    if add_blacklist:
        await message.reply(f"{message.chat.title} successfully added to blacklist")
    else:
        await message.reply("An unknown error occurred")


async def del_blacklist(client, message):
    Tm = await message.reply("Please wait...")
    try:
        if not get_arg(message):
            chat_id = message.chat.id
        else:
            chat_id = int(message.command[1])
        blacklist = await get_chat(client.me.id)
        if chat_id not in blacklist:
            return await message.reply(f"{message.chat.title} is not in the blacklist")
        del_blacklist = await remove_chat(client.me.id, chat_id)
        if del_blacklist:
            await message.reply(f"{chat_id} successfully removed from blacklist")
        else:
            await message.reply("An unknown error occurred")
    except Exception as error:
        await message.reply(str(error))


async def get_blacklist(client, message):
    Tm = await message.reply("Please wait...")
    msg = f"<b>• Total blacklist {len(await get_chat(client.me.id))}</b>\n\n"
    for X in await get_chat(client.me.id):
        try:
            get = await client.get_chat(X)
            msg += f"<b>• {get.title} | <code>{get.id}</code></b>\n"
        except:
            msg += f"<b>• <code>{X}</code></b>\n"
    await Tm.delete()
    await message.reply(msg)


async def rem_all_blacklist(client, message):
    msg = await message.reply("Processing...", quote=True)
    get_bls = await get_chat(client.me.id)
    if len(get_bls) == 0:
        return await msg.edit("Your blacklist is empty")
    for X in get_bls:
        await remove_chat(client.me.id, X)
    await msg.edit("All blacklist entries have been successfully removed")


# ========================== #
# DATABASE RESELLER #
# ========================== #


async def seles_user(client, message):
    user_id = await extract_user(message)
    if message.from_user.id not in KYNAN:
        return
    if not user_id:
        return await message.reply("Reply to user's message or provide user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    reseller = await get_seles()
    if user.id in reseller:
        return await message.reply("Already a reseller.")
    added = await add_seles(user.id)
    if added:
        await add_prem(user.id)
        await message.reply(f"✅ {user.mention} is now a reseller")
    else:
        await Tm.delete()
        await message.reply_text("An unknown error occurred")


async def unseles_user(client, message):
    user_id = await extract_user(message)
    if message.from_user.id not in KYNAN:
        return
    if not user_id:
        return await message.reply("Reply to user's message or provide user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    delreseller = await get_seles()
    if user.id not in delreseller:
        return await message.reply("Not found")
    removed = await remove_seles(user.id)
    if removed:
        await remove_prem(user.id)
        await message.reply(f"{user.mention} successfully removed")
    else:
        await Tm.delete()
        await message.reply_text("An unknown error occurred")


async def get_seles_user(client, message):
    text = ""
    count = 0
    if message.from_user.id not in KYNAN:
        return
    for user_id in await get_seles():
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        await message.reply_text("No users found")
    else:
        await message.reply_text(text)


# ========================== #
# DATABASE EXPIRED #
# ========================== #


async def expired_add(client, message):
    
    if message.from_user.id not in KYNAN:
        return 
    user_id, get_day = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply(f"{message.text} user_id/username - hari")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await message.reply(f"{get_id} telah diaktifkan selama {get_day} hari.")


async def expired_cek(client, message):
    user_id = await extract_user(message)
    if message.from_user.id not in KYNAN:
        return
    if not user_id:
        return await message.reply("Pengguna tidak ditemukan")
    expired_date = await get_expired_date(user_id)
    if expired_date is None:
        await message.reply(f"{user_id} belum diaktifkan.")
    else:
        remaining_days = (expired_date - datetime.now()).days
        await message.reply(
            f"{user_id} aktif hingga {expired_date.strftime('%d-%m-%Y %H:%M:%S')}. Sisa waktu aktif {remaining_days} hari."
        )


async def un_expired(client, message):
    user_id = await extract_user(message)
    
    if message.from_user.id not in KYNAN:
        return
    if not user_id:
        return await message.reply("User tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await message.reply(str(error))
    await rem_expired_date(user.id)
    return await message.reply(f"✅ {user.id} expired telah dihapus")


async def bacotan(_, message: Message):
    await message.delete()
    message.from_user.id
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message is not None:
        text = message.reply_to_message.text
    else:
        return await message.reply(
            "<code>Silakan sertakan pesan atau balas pesan yang ingin disiarkan.</code>"
        )
    kntl = 0
    mmk = []
    jmbt = len(await get_served_users())
    babi = await get_served_users()
    for x in babi:
        mmk.append(int(x["user_id"]))
    if OWNER_ID in mmk:
        mmk.remove(OWNER_ID)
    for i in mmk:
        try:
            await bot.send_message(i, text)
            kntl += 1
        except:
            pass
    return await message.reply(
        f"**Berhasil mengirim pesan ke `{kntl}` pengguna, dari `{jmbt}` pengguna.**"
    )

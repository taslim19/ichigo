import asyncio
import time
import random

from pyrogram.errors import (ChatWriteForbidden, FloodWait, PeerIdInvalid,
                             SlowmodeWait)

from ubot import BLACKLIST_CHAT, PY, ambil_daftar, daftar_rndm, get_chat, kureng_kata, kureng_rndm, tambah_kata, tambah_rndm, gen_font, font

from .gcast import get_broadcast_id

spam_gikesan = {}

__MODULE__ = "Auto Broadcast"
__HELP__ = """
Help For Auto Broadcast

• Command: <code>{0}addkata</code> [Reply to message]
• Explanation: Add a word to broadcast list.

• Command: <code>{0}remkata</code> [Give Text]
• Explanation: Remove a word from broadcast list.

• Command: <code>{0}bgcdb</code>
• Explanation: Start random broadcast.

• Command: <code>{0}cekkata</code>
• Explanation: Check broadcast words.

• Command: <code>{0}sgcdb</code>
• Explanation: Stop random broadcast.
"""


async def spam_kontol_gikes_memek(client, gc, kata_list, kirim_kata, index_gikes):
    try:
        while True:
            for _ in range(10):
                #await asyncio.sleep(10)
                try:
                    katanya = index_gikes % len(kata_list)
                    xx = kata_list[katanya]
                    pili_kondom = random.choice(list(font.values()))
                    fnt = gen_font(xx, pili_kondom)
                    kata = f"<b>{fnt}</b>"
                    await client.send_message(gc, kata)
                    index_gikes += 1
                    kirim_kata.append(katanya)
                except (PeerIdInvalid, ChatWriteForbidden, SlowmodeWait):
                    continue

            await asyncio.sleep(180)

    except FloodWait:
        if gc in spam_gikesan:
            task = spam_gikesan[gc]
            task.cancel()
            del spam_gikesan[gc]


@PY.UBOT("bgcdb", sudo=True)
async def _(client, message):
    await message.reply("**Ok, processing started. Type `sgcdb` to stop.**")
    cek_gc = await get_broadcast_id(client, "group")
    blacklist = await get_chat(client.me.id)
    ambil_bang = await ambil_daftar(client.me.id)
    for gc in cek_gc:
        if gc in blacklist or gc in BLACKLIST_CHAT:
            continue

        try:
            kirim_kata = []
            index_gikes = 0

            task = asyncio.create_task(
                spam_kontol_gikes_memek(
                    client,
                    gc,
                    ambil_bang,
                    kirim_kata,
                    index_gikes,
                )
            )
            spam_gikesan[gc] = task
        except Exception as e:
            print(e)

    


@PY.UBOT("addkata", sudo=True)
async def _(client, message):
    if message.reply_to_message:
        kata = message.reply_to_message.text
    else:
        kata = message.text.split(None, 1)[1]
    if not kata:
        return await message.reply_text("**Please provide some text**")
    await tambah_kata(client.me.id, kata)
    await message.reply_text(f"**Added `{kata}` to broadcast words.**")


@PY.UBOT("remkata", sudo=True)
async def _(client, message):
    if message.reply_to_message:
        kata = message.reply_to_message.text
    else:
        kata = message.text.split(None, 1)[1]
    if not kata:
        return await message.reply_text("**Please provide some text**")
    await kureng_kata(client.me.id, kata)
    await message.reply_text(f"**Removed `{kata}` from broadcast words.**")


@PY.UBOT("cekkata", sudo=True)
async def _(client, message):
    gua = await client.get_me()
    data = await ambil_daftar(client.me.id)
    if not data:
        await message.reply_text("**No broadcast words found**")
    else:
        msg = f"Here are your broadcast words `{gua.first_name}`:\n"
        for kata in data:
            msg += f"**-** `{kata}`\n"
        await message.reply_text(msg)


@PY.UBOT("sgcdb", sudo=True)
async def _(client, message):
    cek_gc = await get_broadcast_id(client, "group")
    for chat_id in cek_gc:
        if chat_id in spam_gikesan:
            task = spam_gikesan[chat_id]
            task.cancel()
            del spam_gikesan[chat_id]
    await message.reply("**Ok, stopped.**")

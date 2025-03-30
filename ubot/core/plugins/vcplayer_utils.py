from datetime import timedelta
from yt_dlp import YoutubeDL
from pytgcalls.types import MediaStream, AudioQuality
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pyrogram import Client

from Ubot import *

PLAYLIST = {}

async def start_next_song(client, chat_id):
    if chat_id in PLAYLIST and PLAYLIST[chat_id]:
        next_song = PLAYLIST[chat_id][0]
        audio_url, title, duration = next_song

        try:
            await client.send_message(
                chat_id,
                f"▶️ <b>Memutar:</b> {title}\n"
                f"⏳ <b>Durasi:</b> {timedelta(seconds=duration)}"
            )
        except Exception as e:
            print(f"❌ Gagal mengirim pesan: {e}")

        try:
            await client.call_py.join_call(chat_id)
        except AlreadyJoinedError:
            pass
        except NoActiveGroupCall:
            return await client.send_message(chat_id, "⚠️ Tidak ada panggilan suara aktif.")

        try:
            await client.call_py.play(chat_id, MediaStream(audio_url, AudioQuality.HIGH))
        except Exception as e:
            print(f"❌ Gagal memutar lagu: {e}")

async def auto_next(client, update):
    """Dipanggil saat lagu selesai, otomatis memutar lagu berikutnya."""
    chat_id = update.chat_id
    if chat_id in PLAYLIST and PLAYLIST[chat_id]:
        PLAYLIST[chat_id].pop(0)
        if PLAYLIST[chat_id]:  
            await start_next_song(client, chat_id)
        else:
            await stop_vc(client, None)

async def stop_vc(client, message):
    chat_id = message.chat.id if message else update.chat_id
    if chat_id in PLAYLIST:
        PLAYLIST.pop(chat_id, None)
    try:
        await client.call_py.leave_call(chat_id)
    except NoActiveGroupCall:
        if message:
            await message.reply("⚠️ Tidak ada panggilan suara aktif.")
    
    if message:
        await message.reply("⏹️ Musik Dihentikan dan Playlist Dihapus.") 

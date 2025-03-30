import re
import requests
from datetime import timedelta
from yt_dlp import YoutubeDL
from pytgcalls.types import MediaStream, AudioQuality
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pyrogram import Client, filters
from pyrogram.types import Message

from Ubot import *

MODULE = "vcplayer"
HELP = """
<b>『 Bantuan vcplayer 』</b>

  <b>• Perintah:</b> <code>{0}play [judul/link]</code>
  <b>• Penjelasan:</b> Memutar musik di obrolan suara
  
  <b>• Perintah:</b> <code>{0}playlist</code>
  <b>• Penjelasan:</b> Menampilkan daftar lagu dalam playlist
  
  <b>• Perintah:</b> <code>{0}skip</code>
  <b>• Penjelasan:</b> Melewati lagu yang sedang diputar
  
  <b>• Perintah:</b> <code>{0}end</code>
  <b>• Penjelasan:</b> Menghentikan musik dan menghapus playlist
"""

PLAYLIST = {}

@PY.UBOT("play")
async def play_vc(client: Client, message: Message):
    msg = await message.reply("<code>Mencari dan memutar musik...</code>")

    if len(message.command) < 2:
        return await msg.edit("❌ Harap masukkan judul lagu atau link YouTube.")

    query = " ".join(message.command[1:])

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "default_search": "ytsearch1",
        "cookiefile": "cookies.txt",  
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)

        if not info or "url" not in info:
            return await msg.edit("❌ Gagal mendapatkan data lagu. Coba lagi.")

        audio_url = info["url"]
        title = info.get("title", "Judul Tidak Diketahui")
        duration = info.get("duration", 0)
        views = info.get("view_count", 0)
        channel = info.get("uploader", "Tidak Diketahui")
        link = info.get("webpage_url", "#")

        song_data = (audio_url, title, duration)

        chat_id = message.chat.id
        if chat_id not in PLAYLIST:
            PLAYLIST[chat_id] = []
        
        PLAYLIST[chat_id].append(song_data)

        if len(PLAYLIST[chat_id]) == 1:
            await start_next_song(client, chat_id)

        await msg.edit(
            f"<b>💡 ɪɴꜰᴏʀᴍᴀsɪ {title}</b>\n\n"
            f"<b>🏷 ɴᴀᴍᴀ:</b> {title}\n"
            f"<b>🧭 ᴅᴜʀᴀsɪ:</b> {timedelta(seconds=duration)}\n"
            f"<b>👀 ᴅɪʟɪʜᴀᴛ:</b> {views:,}\n"
            f"<b>📢 ᴄʜᴀɴɴᴇʟ:</b> {channel}\n"
            f"<b>🔗 ᴛᴀᴜᴛᴀɴ:</b> <a href='{link}'>ʏᴏᴜᴛᴜʙᴇ</a>\n\n"
            f"<b>⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ:</b> {channel}"
        )

    except Exception as e:
        await msg.edit(f"❌ Terjadi kesalahan: {e}")
      
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
          
@PY.UBOT("skip")
async def skip_vc(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in PLAYLIST or not PLAYLIST[chat_id]:
        return await message.reply("❌ Tidak ada lagu untuk dilewati.")

    PLAYLIST[chat_id].pop(0)
    if PLAYLIST[chat_id]:  
        await start_next_song(client, chat_id)
    else:
        await stop_vc(client, message)

@PY.UBOT("end")
async def stop_vc(client, message: Message):
    chat_id = message.chat.id
    if chat_id in PLAYLIST:
        PLAYLIST.pop(chat_id, None)
try:
        await client.call_py.leave_call(chat_id)
    except NoActiveGroupCall:
        await message.reply("⚠️ Tidak ada panggilan suara aktif.")
    
    await message.reply("⏹️ Musik Dihentikan dan Playlist Dihapus.")

@PY.UBOT("playlist")
async def show_playlist(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in PLAYLIST or not PLAYLIST[chat_id]:
        return await message.reply("📭 Playlist kosong.")

    playlist_text = "<b>🎶 Playlist Saat Ini:</b>\n"
    for i, song in enumerate(PLAYLIST[chat_id], 1):
        title = song[1]
        duration = timedelta(seconds=song[2])
        playlist_text += f"\n🎵 <b>{i}. {title}</b> - {duration}"

    await message.reply(playlist_text)

async def auto_next(client, update):
    """Dipanggil saat lagu selesai, otomatis memutar lagu berikutnya."""
    chat_id = update.chat_id
    if chat_id in PLAYLIST and PLAYLIST[chat_id]:
        PLAYLIST[chat_id].pop(0)
        if PLAYLIST[chat_id]:  
            await start_next_song(client, chat_id)
        else:
            await stop_vc(client, None)

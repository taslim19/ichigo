from datetime import timedelta
from yt_dlp import YoutubeDL
from pytgcalls.types import MediaStream, AudioQuality
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram import Client
from pyrogram.types import Message

PLAYLIST = {}

async def start_next_song(client, chat_id):
    if chat_id in PLAYLIST and PLAYLIST[chat_id]:
        next_song = PLAYLIST[chat_id][0]
        audio_url, title, duration = next_song

        try:
            await client.send_message(
                chat_id,
                f"▶️ <b>Now Playing:</b> {title}\n"
                f"⏳ <b>Duration:</b> {timedelta(seconds=duration)}"
            )
        except Exception as e:
            print(f"❌ Failed to send message: {e}")

        try:
            await client.call_py.join_call(chat_id)
        except Exception as e:
            if "already joined" in str(e).lower():
                pass
            else:
                return await client.send_message(chat_id, "⚠️ No active voice chat.")

        try:
            await client.call_py.play(chat_id, MediaStream(audio_url, AudioQuality.HIGH))
        except Exception as e:
            print(f"❌ Failed to play song: {e}")

async def stop_vc(client, message, chat_id=None):
    if chat_id is None and message:
        chat_id = message.chat.id
    elif chat_id is None:
        return

    if chat_id in PLAYLIST:
        PLAYLIST.pop(chat_id, None)
    try:
        await client.call_py.leave_call(chat_id)
    except NoActiveGroupCall:
        if message:
            await message.reply("⚠️ No active voice chat.")
    
    if message:
        await message.reply("⏹️ Music stopped and playlist cleared.")

async def play_vc(client: Client, message: Message):
    msg = await message.reply("<code>Searching and playing music...</code>")

    if len(message.command) < 2:
        return await msg.edit("❌ Please enter a song title or YouTube link.")

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
            return await msg.edit("❌ Failed to get song data. Please try again.")

        audio_url = info["url"]
        title = info.get("title", "Unknown Title")
        duration = info.get("duration", 0)
        views = info.get("view_count", 0)
        channel = info.get("uploader", "Unknown")
        link = info.get("webpage_url", "#")

        song_data = (audio_url, title, duration)

        chat_id = message.chat.id
        if chat_id not in PLAYLIST:
            PLAYLIST[chat_id] = []
        
        PLAYLIST[chat_id].append(song_data)

        if len(PLAYLIST[chat_id]) == 1:
            await start_next_song(client, chat_id)

        await msg.edit(
            f"<b>💡 Song Information</b>\n\n"
            f"<b>🏷 Title:</b> {title}\n"
            f"<b>🧭 Duration:</b> {timedelta(seconds=duration)}\n"
            f"<b>👀 Views:</b> {views:,}\n"
            f"<b>📢 Channel:</b> {channel}\n"
            f"<b>🔗 Link:</b> <a href='{link}'>YouTube</a>\n\n"
            f"<b>⚡ Powered by:</b> {channel}"
        )

    except Exception as e:
        await msg.edit(f"❌ An error occurred: {e}")

async def skip_vc(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in PLAYLIST or not PLAYLIST[chat_id]:
        return await message.reply("❌ No songs to skip.")

    PLAYLIST[chat_id].pop(0)
    if PLAYLIST[chat_id]:  
        await start_next_song(client, chat_id)
    else:
        await stop_vc(client, message, chat_id)

async def end_vc(client, message: Message):
    await stop_vc(client, message, message.chat.id)

async def show_playlist(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in PLAYLIST or not PLAYLIST[chat_id]:
        return await message.reply("📭 Playlist is empty.")

    playlist_text = "<b>🎶 Current Playlist:</b>\n"
    for i, song in enumerate(PLAYLIST[chat_id], 1):
        title = song[1]
        duration = timedelta(seconds=song[2])
        playlist_text += f"\n🎵 <b>{i}. {title}</b> - {duration}"

    await message.reply(playlist_text) 

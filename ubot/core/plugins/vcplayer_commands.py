from datetime import timedelta
from yt_dlp import YoutubeDL
from pytgcalls.types import MediaStream, AudioQuality
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram import Client
from pyrogram.types import Message
import asyncio
import os

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
            # First try to get the call status
            try:
                await client.call_py.get_call(chat_id)
            except NoActiveGroupCall:
                # If not in call, try to join
                await client.call_py.join_call(chat_id)
                print(f"Successfully joined call in {chat_id}")

            # Wait a bit before playing
            await asyncio.sleep(1)

            # Set up audio stream with specific parameters
            await client.call_py.play(
                chat_id,
                MediaStream(
                    audio_url,
                    AudioQuality.HIGH,
                    video_parameters=None,
                    audio_parameters={
                        "bitrate": 48000,
                        "channels": 2,
                        "sample_rate": 48000
                    },
                    stream_type=1
                )
            )
            print(f"Successfully started playing in {chat_id}")
        except Exception as e:
            print(f"Error in voice chat: {e}")
            if "already joined" in str(e).lower():
                try:
                    await client.call_py.play(
                        chat_id,
                        MediaStream(
                            audio_url,
                            AudioQuality.HIGH,
                            video_parameters=None,
                            audio_parameters={
                                "bitrate": 48000,
                                "channels": 2,
                                "sample_rate": 48000
                            },
                            stream_type=1
                        )
                    )
                except Exception as play_error:
                    print(f"Failed to play after join: {play_error}")
                    return await client.send_message(chat_id, "❌ Failed to play song. Please try again.")
            else:
                return await client.send_message(chat_id, "⚠️ Failed to join voice chat. Please make sure:\n1. Voice chat is started\n2. You are in the voice chat")

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
    msg = await message.reply("<code>Searching and downloading music...</code>")

    if len(message.command) < 2:
        return await msg.edit("❌ Please enter a song title or YouTube link.")

    query = " ".join(message.command[1:])
    chat_id = message.chat.id

    # Create downloads directory if it doesn't exist
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "default_search": "ytsearch1",
        "cookiefile": "cookies.txt",
        "extract_flat": True,
        "no_warnings": True,
        "prefer_insecure": True,
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }

    try:
        # First check if we're already in a voice chat
        try:
            await client.call_py.get_call(chat_id)
            print(f"Already in voice chat in {chat_id}")
        except NoActiveGroupCall:
            # If not in voice chat, try to join
            try:
                await client.call_py.join_call(chat_id)
                print(f"Successfully joined call in {chat_id}")
            except Exception as e:
                if "already joined" not in str(e).lower():
                    return await msg.edit("⚠️ Failed to join voice chat. Please make sure:\n1. Voice chat is started\n2. You are in the voice chat")

        # Download the song
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)

        if not info or "url" not in info:
            return await msg.edit("❌ Failed to get song data. Please try again.")

        title = info.get("title", "Unknown Title")
        duration = info.get("duration", 0)
        views = info.get("view_count", 0)
        channel = info.get("uploader", "Unknown")
        link = info.get("webpage_url", "#")

        # Get the downloaded file path
        file_path = f"downloads/{title}.mp3"
        if not os.path.exists(file_path):
            return await msg.edit("❌ Failed to download the song. Please try again.")

        # Wait a bit before playing
        await asyncio.sleep(1)

        # Add to playlist
        song_data = (file_path, title, duration)
        if chat_id not in PLAYLIST:
            PLAYLIST[chat_id] = []
        PLAYLIST[chat_id].append(song_data)

        # Start playing
        try:
            await client.call_py.play(
                chat_id,
                MediaStream(
                    file_path,
                    AudioQuality.HIGH,
                    video_parameters=None,
                    audio_parameters={
                        "bitrate": 48000,
                        "channels": 2,
                        "sample_rate": 48000
                    },
                    stream_type=1
                )
            )
            print(f"Successfully started playing in {chat_id}")
        except Exception as e:
            print(f"Failed to play: {e}")
            return await msg.edit("❌ Failed to play song. Please try again.")

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

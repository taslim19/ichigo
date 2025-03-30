__MODULE__ = "Vcplayer"
__HELP__ = """
<b>『 Vcplayer Help 』</b>

  <b>• Command:</b> <code>{0}play [title/link]</code>
  <b>• Description:</b> Play music in voice chat
  
  <b>• Command:</b> <code>{0}playlist</code>
  <b>• Description:</b> Show current playlist
  
  <b>• Command:</b> <code>{0}skip</code>
  <b>• Description:</b> Skip current song
  
  <b>• Command:</b> <code>{0}end</code>
  <b>• Description:</b> Stop music and clear playlistt
"""

from ubot import PY
from ubot.core.plugins.vcplayer_commands import play_vc, skip_vc, end_vc, show_playlist

@PY.UBOT("play", sudo=True)
async def _(client, message):
    await play_vc(client, message)

@PY.UBOT("skip", sudo=True)
async def _(client, message):
    await skip_vc(client, message)

@PY.UBOT("end", sudo=True)
async def _(client, message):
    await end_vc(client, message)

@PY.UBOT("playlist", sudo=True)
async def _(client, message):
    await show_playlist(client, message) 

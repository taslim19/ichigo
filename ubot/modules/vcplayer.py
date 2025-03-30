__MODULE__ = "Vcplayer"
__HELP__ = """
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

from ubot import *

__MODULE__ = "Youtube"
__HELP__ = """Help For Youtube

• Command: <code>{0}song</code> [song title]
• Explanation: To download the desired music.

• Command: <code>{0}vsong</code> [video title]
• Explanation: To download the desired video.
"""


@PY.UBOT("vsong", sudo=True)
async def _(client, message):
    await vsong_cmd(client, message)


@PY.UBOT("song", sudo=True)
async def _(client, message):
    await song_cmd(client, message)

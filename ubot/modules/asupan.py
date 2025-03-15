from ubot import *

__MODULE__ = "Asupan"
__HELP__ = """
 Help For Intake

• Command: <code>{0}asupan</code>
• Explanation: To send random intake videos.

• Command: <code>{0}bokep</code>
• Explanation: To send random porn videos.

• Command: <code>{0}cewe</code>
• Explanation: To send random girl photos.

• Command: <code>{0}cowo</code>
• Explanation: To send random guy photos.

• Command: <code>{0}anime</code>
• Explanation: To send random anime photos.
"""


@PY.UBOT("asupan", sudo=True)
async def _(client, message):
    await video_asupan(client, message)


@PY.UBOT("cewek", sudo=True)
async def _(client, message):
    await photo_cewek(client, message)


@PY.UBOT("cowok", sudo=True)
async def _(client, message):
    await photo_cowok(client, message)


@PY.UBOT("anime", sudo=True)
async def _(client, message):
    await photo_anime(client, message)


@PY.UBOT("bokep", sudo=True)
async def _(client, message):
    await video_bokep(client, message)

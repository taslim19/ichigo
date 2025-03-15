from ubot import *

__MODULE__ = "Convert"
__HELP__ = """
Help For Convert

• Command: <code>{0}toanime</code> [reply photo/sticker]
• Explanation: Changes image to anime.

• Command: <code>{0}toimg</code> [reply sticker/gif]
• Explanation: Changes sticker/gif to photo.

• Command: <code>{0}tosticker</code> [reply to photo]
• Explanation: Changes photo to sticker.

• Command: <code>{0}togif</code> [reply sticker]
• Explanation: Changes sticker to gif.

• Command: <code>{0}toaudio</code> [reply video]
• Explanation: Changes video to mp3 audio.

• Command: <code>{0}efek</code> [effect code - effect name]
<b>• effect code:</b> <code>bengek</code> <code>robot</code> <code>jedug</code> <code>fast</code> <code>echo</code>
• Explanation: Change the voice note sound.

• Command: <code>{0}curi</code> [reply message]
• Explanation: To steal the timer media, check the saved message
"""


@PY.UBOT("toanime", sudo=True)
async def _(client, message):
    await convert_anime(client, message)


@PY.UBOT("toimg", sudo=True)
async def _(client, message):
    await convert_photo(client, message)


@PY.UBOT("tosticker", sudo=True)
async def _(client, message):
    await convert_sticker(client, message)


@PY.UBOT("togif", sudo=True)
async def _(client, message):
    await convert_gif(client, message)


@PY.UBOT("toaudio", sudo=True)
async def _(client, message):
    await convert_audio(client, message)


@PY.UBOT("efek", sudo=True)
async def _(client, message):
    await convert_efek(client, message)


@PY.UBOT("curi", sudo=True)
async def _(client, message):
    await colong_cmn(client, message)

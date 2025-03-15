from ubot import *

__MODULE__ = "Translate"
__HELP__ = """Help For Translate

• Command: <code>{0}tr</code> [reply/text]
• Explanation: To translate text with the desired country code.

• Command: <code>{0}set_lang</code>
• Explanation: To change the language.

• Command: <code>{0}tts</code> [reply/text]
• Explanation: To translate text with the desired country code and change it into a voice message.
"""


@PY.UBOT("tts", sudo=True)
async def _(client, message):
    await tts_cmd(client, message)


@PY.UBOT("tr|tl", sudo=True)
async def _(client, message):
    await tr_cmd(client, message)


@PY.UBOT("set_lang", sudo=True)
async def _(client, message):
    await set_lang_cmd(client, message)


@PY.INLINE("^ubah_bahasa")
@INLINE.QUERY
async def _(client, inline_query):
    await ubah_bahasa_inline(client, inline_query)


@PY.CALLBACK("^set_bahasa")
@INLINE.DATA
async def _(client, callback_query):
    await set_bahasa_callback(client, callback_query)

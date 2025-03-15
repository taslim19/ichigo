from ubot import *

__MODULE__ = "OpenAi"
__HELP__ = """
 Help For OpenAi

• Command : <code>{0}ai</code> ᴏʀ <code>{0}ask</code> [query]
• Explanation : To use chatgpt.

• Command : <code>{0}dalle</code> ᴏʀ <code>{0}photo</code> [query]
• Explanation : To create a photo.

• Command : <code>{0}stt</code> [audio reply]
• Explanation : To convert voice message to text.
"""


@PY.UBOT("ai|ask", sudo=True)
async def _(client, message):
    await ai_cmd(client, message)


@PY.UBOT("dalle|photo", sudo=True)
async def _(client, message):
    await dalle_cmd(client, message)


@PY.UBOT("stt", sudo=True)
async def _(client, message):
    await stt_cmd(client, message)

from ubot import *

__MODULE__ = "Kang"
__HELP__ = """
 Help for Kang

• Command: <code>{0}kang</code> [reply to sticker]
• Explanation: To make a sticker costume, sir.
"""


# @PY.BOT("kang", sudo=True)
# async def _(client, message):
# await kang_cmd_bot(client, message)


@PY.UBOT("kang", sudo=True)
async def _(client, message):
    await kang(client, message)

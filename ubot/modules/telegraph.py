from ubot import *

__MODULE__ = "Telegraph"
__HELP__ = """Help For Telegraph

• Command: <code>{0}tg</code> [reply media/text]
• Explanation: To upload media/text to telegra.ph.
"""


@PY.UBOT("tg", sudo=True)
async def _(client, message):
    await tg_cmd(client, message)

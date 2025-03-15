from ubot import *

__MODULE__ = "Tiny"
__HELP__ = """Help For Telegraph

• Command: <code>{0}tg</code> [reply media/text]
• Explanation: To upload media/text to telegra.ph.
"""


@PY.UBOT("tiny", sudo=True)
async def _(client, message):
    await tiny_cmd(client, message)

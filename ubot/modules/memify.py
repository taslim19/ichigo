from ubot import *

__MODULE__ = "Memify"
__HELP__ = """Help For Memify

• Command: <code>{0}mmf</code> [text]
• Explanation: To make the image smaller.
"""


@PY.UBOT("mmf|memify", sudo=True)
async def _(client, message):
    await memify_cmd(client, message)

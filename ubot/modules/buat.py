from ubot import *

__MODULE__ = "Create"
__HELP__ = """
Help For Create

• Command: <code>{0}create</code> gc
• Explanation: To create a telegram group.

• Command: <code>{0}create</code> ch
• Explanation: To create a telegram channel.
"""


@PY.UBOT("create", sudo=True)
async def _(client, message):
    await buat_apaam(client, message)

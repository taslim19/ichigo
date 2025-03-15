from ubot import *

__MODULE__ = "Sangmata"
__HELP__ = """
Help for Sangmata

• Command: <code>{cobadah}sg</code> [user_id/reply user]
• Explanation: To check the history of the name/username.
"""


@PY.UBOT("sg", sudo=True)
async def _(client, message):
    await sg_cmd(client, message)

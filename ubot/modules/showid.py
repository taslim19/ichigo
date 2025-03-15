from ubot import *

__MODULE__ = "ShowID"
__HELP__ = """Help For Secret

• Command: <code>{0}msg</code> [reply to user - text]
• Explanation: To send a message secretly.
"""


@PY.UBOT("id", sudo=True)
async def _(client, message):
    await id_cmd(client, message)

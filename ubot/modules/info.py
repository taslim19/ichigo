from ubot import *

__MODULE__ = "Info"
__HELP__ = """Help For Info

• Command: <code>{0}info</code> [user_id/username/reply message]
• Explanation: To view user information.

• Command: <code>{0}cinfo</code> [user_id/username/reply message]
• Explanation: To view chat information.
"""


@PY.UBOT("whois|info", sudo=True)
async def _(client, message):
    await info_cmd(client, message)


@PY.UBOT("cwhois|cinfo", sudo=True)
async def _(client, message):
    await cinfo_cmd(client, message)

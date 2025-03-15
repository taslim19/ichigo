from ubot import *

__MODULE__ = "Mention"
__HELP__ = """Mention Help

• Command: <code>{0}all</code> [type message/reply message]
• Explanation: To mention all group members with the message you want.

• Command: <code>{0}cancel</code>
• Explanation: To cancel mentioning group members.
"""


@PY.UBOT("all", sudo=True)
async def _(client, message):
    await mentionall(client, message)


@PY.UBOT("batal", sudo=True)
async def _(client, message):
    await batal_tag(client, message)

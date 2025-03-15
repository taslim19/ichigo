from ubot import *

__MODULE__ = "Admin"
__HELP__ = """Help For Admin

• Command: <code>{0}kick</code> [user_id/username/reply user]
• Explanation: To kick a member from the group.

• Command: <code>{0}ban</code> [user_id/username/reply user]
• Explanation: To block a member from the group.

• Command: <code>{0}mute</code> [user_id/username/reply user]
• Explanation: To mute a member from the group.

• Command: <code>{0}unban</code> [user_id/username/reply user]
• Explanation: To unblock a member from the group.

• Command: <code>{0}unmute</code> [user_id/username/reply user]
• Explanation: To unmute a member from a group.
"""


@PY.UBOT("kick|ban|mute|unmute|unban", sudo=True)
async def _(client, message):
    await admin_bannen(client, message)


@PY.UBOT("pin|unpin", sudo=True)
async def _(client, message):
    await pin_message(client, message)


@PY.UBOT("promote|fullpromote", sudo=True)
async def _(client, message):
    await promotte(client, message)


@PY.UBOT("demote", sudo=True)
async def _(client, message):
    await demote(client, message)


@PY.UBOT("getlink", sudo=True)
async def _(client, message):
    await invite_link(client, message)

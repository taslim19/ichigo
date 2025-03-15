from ubot import *

__MODULE__ = "Join"
__HELP__ = """
Help To Join

• Command: <code>{0}kickme</code>
• Explanation: To exit the group.

• Command: <code>{0}join</code> [username]
• Explanation: To join a group with a username.

• Command: <code>{0}leaveallgc</code>
• Explanation: To exit all groups of your account.

• Command: <code>{0}leaveallch</code>
• Explanation: To exit all channels of your account.

• Command: <code>{0}leave</code> [username]
• Explanation: To exit a group with a username.
"""


@PY.UBOT("kickme|leave", sudo=True)
async def _(client, message):
    await leave(client, message)


@PY.UBOT("join", sudo=True)
async def _(client, message):
    await join(client, message)


@PY.UBOT("leaveallgc", sudo=True)
async def _(client, message):
    await kickmeall(client, message)


@PY.UBOT("leaveallch", sudo=True)
async def _(client, message):
    await kickmeallch(client, message)

from ubot import *

__MODULE__ = "Purge"
__HELP__ = """Help For Purge

• Command: <code>{0}purge</code> [reply to message]
• Explanation: Purge (delete all messages) chat from the replied message to the last one.

• Command: <code>{0}del</code> [reply to message]
• Explanation: Delete the replied message.

• Command: <code>{0}purgeme</code> [number of messages]
• Explanation: Delete your own messages by specifying the total number of messages.
"""


@PY.UBOT("del", sudo=True)
async def _(client, message):
    await del_cmd(client, message)


@PY.UBOT("purgeme", sudo=True)
async def _(client, message):
    await purgeme_cmd(client, message)


@PY.UBOT("purge", sudo=True)
async def _(client, message):
    await purge_cmd(client, message)

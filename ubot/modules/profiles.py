from ubot import *

__MODULE__ = "Profile"
__HELP__ = """
Help For Profile

• Command: <code>{0}adminlist</code>
• Explanation: To see your group admin status.

• Command: <code>{0}setbio</code> [query]
• Explanation: To change your bio.

• Command: <code>{0}setname</code> [query]
• Explanation: To change your Name.

• Command: <code>{0}setpp</code> [media reply]
• Explanation: To change your Account Photo.

• Command: <code>{0}block</code> [user reply]
• Explanation: To block a user.

• Command: <code>{0}unblock</code> [query]
• Explanation: To unblock a user.
"""


@PY.UBOT("setbio", sudo=True)
async def _(client, message):
    await set_bio(client, message)


@PY.UBOT("setname", sudo=True)
async def _(client, message):
    await setname(client, message)


@PY.UBOT("block", sudo=True)
async def _(client, message):
    await block_user_func(client, message)


@PY.UBOT("unblock", sudo=True)
async def _(client, message):
    await unblock_user_func(client, message)


@PY.UBOT("setpp", sudo=True)
async def _(client, message):
    await set_pfp(client, message)


@PY.UBOT("adminlist", sudo=True)
async def _(client, message):
    await list_admin(client, message)

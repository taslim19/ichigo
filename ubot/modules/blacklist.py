from ubot import *

__MODULE__ = "Blacklist"
__HELP__ = """
Help For Blacklist

• Command: <code>{0}rallbl</code>
• Explanation: Remove all anti gcast

• Command: <code>{0}addbl</code>
• Explanation: Add a group to anti Gcast.

• Command: <code>{0}delbl</code>
• Explanation: Remove a group from the anti Gcast list.

• Command: <code>{0}listbl</code>
• Explanation: View the list of anti Gcast groups.
"""


@PY.UBOT("addbl", sudo=True)
async def _(client, message):
    await add_blaclist(client, message)


@PY.UBOT("delbl", sudo=True)
async def _(client, message):
    await del_blacklist(client, message)


@PY.UBOT("rallbl", sudo=True)
async def _(client, message):
    await rem_all_blacklist(client, message)


@PY.UBOT("listbl", sudo=True)
async def _(client, message):
    await get_blacklist(client, message)

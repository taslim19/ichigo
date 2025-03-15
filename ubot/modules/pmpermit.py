from ubot import *

__MODULE__ = "PMPermit"
__HELP__ = """Help For PMPermit

• Command: <code>{0}antipm</code> [on or off]
• Explanation: To turn antipm on or off

• Command: <code>{0}setmsg</code> [reply or give a message]
• Explanation: To set antipm messages.

• Command: <code>{0}setlimit</code> [number]
• Explanation: To set block message warning.

• Command: <code>{0}ok</code>
• Explanation: To approve a message.

• Command: <code>{0}no</code>
• Explanation: To reject a message.
"""


@PY.UBOT("antipm|pmpermit", sudo=True)
async def _(client, message):
    await permitpm(client, message)


@PY.UBOT("ok|a", sudo=True)
async def _(client, message):
    await approve(client, message)


@PY.UBOT("da|no", sudo=True)
async def _(client, message):
    await disapprove(client, message)


@PY.UBOT("setmsg", sudo=True)
async def _(client, message):
    await set_msg(client, message)


@PY.UBOT("setlimit", sudo=True)
async def _(client, message):
    await set_limit(client, message)


@ubot.on_message(
    filters.private & filters.incoming & ~filters.service & ~filters.me & ~filters.bot
)
async def _(client, message):
    await handle_pmpermit(client, message)

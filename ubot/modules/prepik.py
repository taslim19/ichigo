from ubot import *

__MODULE__ = "Prefix"
__HELP__ = """Help For Prefix

• Command : {0}prefix [trigger]
• Explanation : To set your userbot handler.
"""


@PY.UBOT("prefix", sudo=True)
async def _(client, message):
    await kok_anjeng(client, message)

from ubot import *

__MODULE__ = "Search"
__HELP__ = """Help For Search

• Command: <code>{0}pic</code> [query]
• Explanation: For images with a limit of 5.

• Command: <code>{0}gif</code> [query]
• Explanation: For gif.
"""


@PY.UBOT("bing|pic", sudo=True)
async def _(client, message):
    await pic_bing_cmd(client, message)


@PY.UBOT("gif", sudo=True)
async def _(client, message):
    await gif_cmd(client, message)

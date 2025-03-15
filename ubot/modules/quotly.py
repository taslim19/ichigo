from ubot import *

__MODULE__ = "Quotly"
__HELP__ = """Help For Quotly

• Command: <code>{0}q</code> [text/reply to text/media]
• Explanation: To change text into stickers.

• Command: <code>{0}q</code> [white/black/red/pink]
• Explanation: To change the background of a quote.
"""


@PY.UBOT("q", sudo=True)
async def _(client, message):
    await quotly_cmd(client, message)

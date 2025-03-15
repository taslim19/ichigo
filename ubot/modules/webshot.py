from ubot import *

__MODULE__ = "Webshot"
__HELP__ = """Webshot Help

• Command: <code>{0}ss</code> [link]
• Explanation: To get a screenshot of the link.
"""


@PY.UBOT("webss", sudo=True)
async def _(client, message):
    await take_ss(client, message)

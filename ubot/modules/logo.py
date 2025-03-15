from ubot import *

__MODULE__ = "Logo"
__HELP__ = """
Logo Help

• Command: <code>{0}logo</code> [text]
• Explanation: To create a logo with the word random.

• Command: <code>{0}blogo</code> [text]
• Explanation: To make the background black.
"""


@PY.UBOT("blogo|logo", sudo=True)
async def _(client, message):
    await logo_cmd(client, message)

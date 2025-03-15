from ubot import *

__MODULE__ = "Google"
__HELP__ = """
Help For Google

• Command: <code>{0}google</code> [query]
• Explanation: To search for something.
"""


@PY.UBOT("google", sudo=True)
async def _(client, message):
    await gsearch(client, message)

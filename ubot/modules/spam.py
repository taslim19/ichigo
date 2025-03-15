from ubot import *

__MODULE__ = "Spam"
__HELP__ = """Spam Help

• Command: <code>{0}dspam</code> [amount] [delay time] [reply message]
• Explanation: To delay spam.

• Command: <code>{0}spam</code> [amount] [word]
• Explanation: To spam.

• Command: <code>{0}cspam</code>
• Explanation: To stop spam.
"""


@PY.UBOT("spam|dspam", sudo=True)
async def _(client, message):
    if message.command[0] == "spam":
        await spam_cmd(client, message)
    if message.command[0] == "dspam":
        await dspam_cmd(client, message)


@PY.UBOT("cspam", sudo=True)
async def _(client, message):
    await capek_dah(client, message)

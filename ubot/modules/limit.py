from ubot import *

__MODULE__ = "Limit"
__HELP__ = """
Help for Limits

• Command: <code>{0}limit</code>
• Explanation: To check whether your account is limited or not.
"""


@PY.UBOT("limit", sudo=True)
async def _(client, message):
    await limit_cmd(client, message)

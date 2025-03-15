from ubot import *

__MODULE__ = "Staff"
__HELP__ = """Staff Help

• Command: <code>{0}staff</code>
• Explanation: To find out the list of all admins in the group.
"""


@PY.UBOT("staff", sudo=True)
async def _(client, message):
    await staff_cmd(client, message)

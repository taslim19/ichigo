from ubot import *

__MODULE__ = "Zombies"
__HELP__ = """Help For Zombies

• Command: <code>{0}zombies</code>
• Explanation: To remove depressed accounts from your group.
"""


@PY.UBOT("zombies", sudo=True)
async def _(client, message):
    await zombies_cmd(client, message)

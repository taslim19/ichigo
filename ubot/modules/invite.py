from ubot import *

__MODULE__ = "Invite"
__HELP__ = """
Help For Invite

• Command: <code>{0}invite</code> [username]
• Explanation: To invite members to the group.

• Command: <code>{0}inviteall</code> [group username - cooldwon - members]
• Explanation: To invite members to your group.

• Command: <code>{0}cancel</code>
• Explanation: To cancel the invite process.
  """


@PY.UBOT("invite", sudo=True)
async def _(client, message):
    await invite_cmd(client, message)


@PY.UBOT("inviteall", sudo=True)
async def _(client, message):
    await inviteall_cmd(client, message)


@PY.UBOT("cancel", sudo=True)
async def _(client, message):
    await cancel_cmd(client, message)

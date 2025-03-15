from ubot import *

__MODULE__ = "VoiceChat"
__HELP__ = """Voice Chat Help

• Command: <code>{0}startvc</code>
• Explanation: To start a group voice chat.

• Command: <code>{0}stopvc</code>
• Explanation: To end a group voice chat.

• Command: <code>{0}joinvc</code>
• Explanation: To join a group voice chat.

• Command: <code>{0}leavevc</code>
• Explanation: To leave a group voice chat.
"""


@PY.UBOT("startvc", sudo=True)
async def _(client, message):
    await start_vctools(client, message)


@PY.UBOT("stopvc", sudo=True)
async def _(client, message):
    await stop_vctools(client, message)


@PY.UBOT("joinvc", sudo=True)
async def _(client, message):
    await join_os(client, message)


@PY.UBOT("leavevc", sudo=True)
async def _(client, message):
    await turun_os(client, message)

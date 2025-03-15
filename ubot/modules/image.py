from ubot import *

__MODULE__ = "Image"
__HELP__ = """
Image Help

• Command: <code>{0}rbg</code> [reply to photo]
• Explanation: To remove the background of the image.

• Command: <code>{0}blur</code> [reply to photo]
• Explanation: To give a blur effect to the image.

• Command: <code>{0}miror</code> [reply to photo]
• Explanation: To give a mirror effect to the image.

• Command: <code>{0}negative</code> [reply to photo]
• Explanation: To give a negative effect to the image.
"""


@PY.UBOT("rbg", sudo=True)
async def _(client, message):
    await rbg_cmd(client, message)


@PY.UBOT("blur", sudo=True)
async def _(client, message):
    await blur_cmd(client, message)


@PY.UBOT("negative", sudo=True)
async def _(client, message):
    await negative_cmd(client, message)


@PY.UBOT("miror", sudo=True)
async def _(client, message):
    await miror_cmd(client, message)

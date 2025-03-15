from ubot import *

__MODULE__ = "Sosmed"
__HELP__ = """Help For Social Media

• Command: <code>{0}sosmed</code> [link]
• Explanation: To Download Media From Facebook/Tiktok/Instagram/Twitter/YouTube.
"""


@PY.UBOT("sosmed", sudo=True)
async def _(client, message):
    await sosmed_cmd(client, message)

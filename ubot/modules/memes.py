from ubot import *

__MODULE__ = "Meme"
__HELP__ = """
Help For Memes

• Command: <code>{0}memes</code> [text]
• Explanation: To create random memes words.
"""


@PY.UBOT("mms|memes", sudo=True)
async def _(client, message):
    await memes_cmd(client, message)

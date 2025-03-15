from ubot import *

__MODULE__ = "Read"
__HELP__ = """Help For Ocr

• Command : <code>{0}ocr</code> [media reply]
• Explanation : To read text from media.
"""


@PY.UBOT("ocr", sudo=True)
async def _(client, message):
    await read_cmd(client, message)

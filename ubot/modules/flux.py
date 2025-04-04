__MODULE__ = "Flux"
__HELP__ = """Help For Flux

• Command: <code>{0}flux</code> [query/reply user]
• Explanation: Generates an image based on the given query using the FLUX API.

"""
from ubot import PY
from ubot.core.plugins.flx import flux_func


@PY.UBOT("flux", sudo=True)
async def _(client, message):
    await flux_func(client, message)

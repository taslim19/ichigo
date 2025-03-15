from ubot import *

__MODULE__ = "Notes"
__HELP__ = """Help For Notes

• Command: <code>{0}save</code> [name - reply message]
• Explanation: To save a note.

• Command: <code>{0}get</code> [name]
• Explanation: To retrieve a saved note.

• Command: <code>{0}rm</code> [name]
• Explanation: To delete a note name.

• Command: <code>{0}notes</code>
• Explanation: To see a list of saved notes.

• Note: To use the button, use the format:
<code>Mbah google [google|google.com]</code>
"""


@PY.UBOT("save", sudo=True)
async def _(client, message):
    await addnote_cmd(client, message)


@PY.UBOT("get", sudo=True)
async def _(client, message):
    await get_cmd(client, message)


@PY.INLINE("^get_notes")
@INLINE.QUERY
async def _(client, inline_query):
    await get_notes_button(client, inline_query)


@PY.UBOT("rm", sudo=True)
async def _(client, message):
    await delnote_cmd(client, message)


@PY.UBOT("notes", sudo=True)
async def _(client, message):
    await notes_cmd(client, message)

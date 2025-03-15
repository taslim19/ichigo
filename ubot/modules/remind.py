"""
CREDIT
KODE BY [AMANG] <https://t.me/amwang> <https://github.com/amanqs>
HAPUS CREDIT?, WAH KEBANGETAN SIH.
"""


from ubot import *

__MODULE__ = "Reminders"
__HELP__ = """This module allows users to set reminders.

• Command: `{0}remind`
• Description: Sets a reminder for a specific time in the future.

Usage: `{0}remind <time> <message>`
Example:
`{0}remind 1h30m Buy milk`

`{0}remind 1h30m Check email`

Note: The time argument supports multiple formats such as hours (h), minutes (m), and days (d).

• Command: `{0}listremind`
• Description: Displays a list of saved reminders.

Usage: `{0}listremind`
To set a reminder, use the `{0}remind` command followed by the desired time and message. The time argument must be provided in the format mentioned above. The reminder will be sent at the specified time with the given message.

To view a list of saved reminders, use the `{0}listremind` command.
"""


@PY.UBOT("remind", sudo=True)
async def _(client, message):
    await reminder(client, message)


@PY.UBOT("listremind", sudo=True)
async def _(client, message):
    await listrem(client, message)

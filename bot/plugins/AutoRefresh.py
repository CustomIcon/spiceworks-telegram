from bot import bot
from pyrogram import types

text = """
#{ticket_id}
Created at {created_at} by {creator_firstname} {creator_lastname} ({creator_email})
Assigned to {assignee}
--**{summary}**--
__{description}__
"""

async def AutoRefresh():
    ...
from json import decoder

from pyrogram import filters, types

from bot import bot
from bot.utils import GetOpt
from spiceworks.types import Ticket

text = """
#{ticket_id}
Created at {created_at} by {creator_firstname} {creator_lastname} ({creator_email})
Assigned to {assignee}
--**{summary}**--
__{description}__
"""


@bot.on_message(filters.user(bot.config.getint('spiceworks-bot', 'owner_id')) & filters.command('ticket'))
async def _(_, message: types.Message):
    tickets = message.text.split(None, 1)[1] if len(message.command,) != 1 else await bot.get_tickets(filter_id=Ticket.OPEN)
    if isinstance (tickets, list):
        ticket = tickets[0]
    else:
        ticket = await bot.get_tickets(int(message.command[1]))
    reply_markup = [
            [
                types.InlineKeyboardButton('Previous', f'ticket_{ticket["id"] - 1}'),
                types.InlineKeyboardButton('Next', f'ticket_{ticket["id"] + 1}'),
            ],
            [
                types.InlineKeyboardButton(
                    '🌐 Open in Web',
                    url=bot.config.get("spiceworks-help-desk", "host") + "/tickets/list/single_ticket/" + str(ticket["id"])
                ),
            ]
        ]
    reply_markup.append(GetOpt(status=ticket["status"]))
    return await message.reply(
        text=text.format(
            ticket_id=ticket["id"],
            created_at=ticket["created_at"],
            creator_firstname=ticket["creator"]["first_name"],
            creator_lastname=ticket["creator"]["last_name"],
            creator_email=ticket["creator"]["email"],
            assignee=ticket["assignee"]["email"],
            summary=ticket["summary"],
            description=ticket['description']
        ),
        reply_markup=types.InlineKeyboardMarkup(reply_markup)
    )


@bot.on_callback_query(filters.regex("^ticket_"))
async def _(_, query: types.CallbackQuery):
    try:
        ticket = (await bot.get_tickets(int(query.data.split("_")[1])))
    except decoder.JSONDecodeError:
        return await query.answer("That is the End of All tickets!", show_alert=True)
    reply_markup = [
            [
                types.InlineKeyboardButton('Previous', f'ticket_{ticket["id"] - 1}'),
                types.InlineKeyboardButton('Next', f'ticket_{ticket["id"] + 1}'),
            ],
            [
                types.InlineKeyboardButton(
                    '🌐 Open in Web',
                    url=bot.config.get("spiceworks-help-desk", "host") + "/tickets/list/single_ticket/" + str(ticket["id"])
                ),
            ]
        ]
    reply_markup.append(GetOpt(status=ticket["status"]))
    return await query.message.edit(
        text=text.format(
            ticket_id=ticket["id"],
            created_at=ticket["created_at"],
            creator_firstname=ticket["creator"]["first_name"],
            creator_lastname=ticket["creator"]["last_name"],
            creator_email=ticket["creator"]["email"],
            assignee=ticket["assignee"]["email"],
            summary=ticket["summary"],
            description=ticket['description']
        ),
        reply_markup=types.InlineKeyboardMarkup(reply_markup)
    )


@bot.on_inline_query(filters.user(bot.config.getint('spiceworks-bot', 'owner_id')))
async def _(_, query: types.InlineQuery):
    if query.query.lower() == "closed":
        tickets = (await bot.get_tickets(filter_id=Ticket.CLOSED))
    elif query.query.lower() == "open":
        tickets = (await bot.get_tickets(filter_id=Ticket.OPEN))
    else:
        return
    queue = [
        types.InlineQueryResultArticle(
            title=f"{ticket['id']} {ticket['summary']}",
            description=f'Assigned by: {ticket["creator"]["email"]}',
            input_message_content=types.InputTextMessageContent(f"/ticket {ticket['id']}")
        ) for ticket in tickets
    ]

    return await query.answer(
        results=queue,
        cache_time=0
    )


@bot.on_message(filters.user(bot.config.getint('spiceworks-bot', 'owner_id')) & filters.command('start'))
async def _(_, message: types.Message):
    tickets = await bot.get_tickets()
    open_tickets = []
    closed_tickets = []
    for ticket in tickets:
        if ticket["status"] == "closed":
            closed_tickets.append(ticket)
        else:
            open_tickets.append(ticket)
    return await message.reply(
        "Please select an option from down below",
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(f'Open Tickets - {len(open_tickets)}', switch_inline_query_current_chat="open")
                ],
                [
                    types.InlineKeyboardButton(f'Closed Tickets - {len(closed_tickets)}', switch_inline_query_current_chat="closed")
                ]
            ]
        )
    )

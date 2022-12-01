from pyrogram import types

def GetOpt(status: str, ticket_id: int):
    return [
        types.InlineKeyboardButton(
            '❌ Close', f'operation_close_{ticket_id}'
        ),
        ] if status == "open" else [
            types.InlineKeyboardButton(
                '🔓 Re-Open',
                f'operation_open_{ticket_id}'
            ),
        ]

from pyrogram import types

def GetOpt(status: str):
    return [
        types.InlineKeyboardButton(
            '❌ Close', 'operation_close'
        ),
        ] if status == "open" else [
            types.InlineKeyboardButton(
                '🔓 Re-Open',
                'operation_open'
            ),
        ]

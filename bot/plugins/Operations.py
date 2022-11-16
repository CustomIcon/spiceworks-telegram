from bot import bot
from pyrogram import filters, types


@bot.on_callback_query(filters.regex("^operation_"))
async def _(_, query: types.CallbackQuery):
    return await query.answer("Not Implemented yet!", show_alert=True)
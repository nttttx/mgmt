from telebot import types
from telebot.async_telebot import AsyncTeleBot


async def start_handler(
    message: types.Message,
    bot: AsyncTeleBot,
) -> None:
    """Handler for /start command"""
    myself = await bot.get_me()
    text = "Welcome to %s" % myself.first_name

    await bot.reply_to(message, text)


__all__ = ["start_handler"]

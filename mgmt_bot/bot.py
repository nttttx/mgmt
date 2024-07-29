from telebot.async_telebot import AsyncTeleBot
from .config import config
from . import handlers
import asyncio
import logging

log = logging.getLogger(__name__)
bot = AsyncTeleBot(
    config["BOT_TOKEN"],
    parse_mode="HTML"
)


def register_handlers() -> None:
    log.debug("register_handlers()")

    bot.register_message_handler(
        handlers.start_handler,
        commands=["start"],
        pass_bot=True
    )

    bot.register_message_handler(
        handlers.ban_handler,
        commands=["ban"],
        chat_types=[
            "group",
            "supergroup"
        ],
        pass_bot=True
    )
    bot.register_message_handler(
        handlers.kick_handler,
        commands=["kick"],
        chat_types=[
            "group",
            "supergroup"
        ],
        pass_bot=True
    )
    bot.register_message_handler(
        handlers.mute_handler,
        commands=["mute"],
        chat_types=[
            "group",
            "supergroup"
        ],
        pass_bot=True
    )

    bot.register_message_handler(
        handlers.id_handler,
        commands=["id"],
        chat_types=[
            "group",
            "supergroup"
        ],
        pass_bot=True
    )


def bot_main() -> None:
    register_handlers()
    log.debug(".polling()")
    asyncio.run(bot.polling())


__all__ = ["bot_main"]

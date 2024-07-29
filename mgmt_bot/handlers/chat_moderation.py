from telebot.async_telebot import AsyncTeleBot
from telebot import types
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# Shitty implementation..
# Maybe pytba has this type of function built in
async def _is_admin(
    message: types.Message,
    bot: AsyncTeleBot
) -> bool:
    """Check if user is an administrator
    Args:
        message (types.Message): Message sent by user
        bot (AsyncTelebot): Instance of a bot"""

    user = message.from_user
    log.debug("Checking if %s is an administrator" % user.id)
    administrators = await bot.get_chat_administrators(
        message.chat.id
    )
    for admin in administrators:
        log.debug("Checking %s" % admin.user.id)
        if admin.user.id == user.id:
            return True
    log.info("%s is not an administrator." % user.id)
    return False



async def _ban_user(
    message: types.Message,
    user_to_ban: types.User,
    bot: AsyncTeleBot
) -> None:
    log.info("Banning %s..." % user_to_ban.id)
    await bot.ban_chat_member(message.chat.id, user_to_ban.id)
    await bot.reply_to(message, "Banned %s" % user_to_ban.first_name)


async def _kick_user(
    message: types.Message,
    user_to_kick: types.User,
    bot: AsyncTeleBot
) -> None:
    log.info("Kicking %s..." % user_to_kick.id)
    await bot.kick_chat_member(message.chat.id, user_to_kick.id)
    await bot.reply_to(message, "Kicked %s" % user_to_kick.first_name)


async def ban_handler(
    message: types.Message,
    bot: AsyncTeleBot
) -> None:
    """Handler for /ban command"""

    if not await _is_admin(message, bot):
        bot.reply_to(message, "Not an admin.")
        return
    if message.reply_to_message:
        user_to_ban = message.reply_to_message.from_user
        await _ban_user(
            message,
            user_to_ban,
            bot
        )
    elif len(message.text.split()) >= 2:
        # We expect that user is second entity in message
        # /ban 123123123
        #      ^^^^^^^^^ this one
        message_splitted = message.text.split()
        try:
            user_to_ban_id = int(message_splitted[1])
            member_to_ban = await bot.get_chat_member(
                message.chat.id,
                user_to_ban_id
            )
            await _ban_user(
                message,
                member_to_ban.user,
                bot
            )
        except ValueError:
            await bot.reply_to(message, "Id must be an integer")


async def kick_handler(
    message: types.Message,
    bot: AsyncTeleBot
) -> None:
    """Handler for /kick command"""

    if not await _is_admin(message, bot):
        bot.reply_to(message, "Not an admin.")
        return
    if message.reply_to_message:
        user_to_kick = message.reply_to_message.from_user
        await _kick_user(
            message,
            user_to_kick,
            bot
        )
    elif len(message.text.split()) >= 2:
        # We expect that user is second entity in message
        # /kick 123123123
        #       ^^^^^^^^^ this one
        message_splitted = message.text.split()
        try:
            user_to_kick_id = int(message_splitted[1])
            member_to_kick = await bot.get_chat_member(
                message.chat.id,
                user_to_kick_id
            )
            await _kick_user(
                message,
                member_to_kick.user,
                bot
            )
        except ValueError:
            await bot.reply_to(message, "Id must be an integer")



__all__ = [
    "ban_handler",
    "kick_handler"
]

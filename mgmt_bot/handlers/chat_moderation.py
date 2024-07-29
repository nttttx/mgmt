from telebot.async_telebot import AsyncTeleBot
from telebot import types
from mgmt_bot import tools
import datetime
import logging
import time

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
        message (types.Message): Message sent by the user
        bot (AsyncTelebot): Instance of a bot
    Returns:
        bool: User is admin"""

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


async def _get_ban_duration(
    message: types.Message,
    readable_time: list[str],
    bot: AsyncTeleBot
) -> int:
    """Get ban duration and notify user if something is wrong
    Args:
        message (types.Message): Message sent by the user.
        readable_time (list[str]): Readable time list (ex. "1h 2m")
        bot (AsyncTeleBot): Instance of a bot
    Returns:
        int: Ban duration
    Exception:
        ValueError: User sent wrong wrong time stringj"""

    try:
        duration = tools.convert_human_time_string(readable_time)
    except Exception as e:
        await bot.reply_to(
            message,
            (
                "Invalid time declaration. "
                "Pass human readable time. (example: \"1s 1m 1h 1d 1w 1M 1y\")"
            )
        )
        raise ValueError from e
    return duration


async def _ban_user(
    message: types.Message,
    user_to_ban: types.User,
    duration: int,
    bot: AsyncTeleBot
) -> None:
    log.info("Banning %s... Duration: %s" % (user_to_ban.id, duration))
    unban_time = time.time() + duration

    await bot.ban_chat_member(
        message.chat.id,
        user_to_ban.id,
        until_date=unban_time
    )

    await bot.reply_to(
        message,
        "Banned %s (Duration: %s)" % (
            user_to_ban.first_name,

            str(datetime.timedelta(seconds=duration))
            if duration > 3
            else "Forever"
        )
    )


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

    message_splitted = message.text.split()

    if not await _is_admin(message, bot):
        bot.reply_to(message, "Not an admin.")
        return

    if message.reply_to_message:
        user_to_ban = message.reply_to_message.from_user
        if len(message_splitted) > 1:
            duration = await _get_ban_duration(
                message,
                message_splitted[1:],
                bot
            )
        else:
            duration = 0

        await _ban_user(
            message,
            user_to_ban,
            duration,
            bot
        )
    elif len(message_splitted) > 1:
        # We expect that user is second entity in message
        # /ban 123123123
        #      ^^^^^^^^^ this one
        if len(message_splitted) > 2:
            duration = await _get_ban_duration(
                message,
                message_splitted[2:],
                bot
            )
        else:
            duration = 0
        try:
            user_to_ban_id = int(message_splitted[1])
            member_to_ban = await bot.get_chat_member(
                message.chat.id,
                user_to_ban_id
            )
            await _ban_user(
                message,
                member_to_ban.user,
                duration,
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

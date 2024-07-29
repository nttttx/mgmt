from telebot.async_telebot import AsyncTeleBot
from telebot import types
from mgmt_bot import tools
import datetime
import logging
import time

log = logging.getLogger(__name__)


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
        ValueError: User sent wrong wrong time string"""

    try:
        duration = tools.convert_human_time_string(readable_time)
    except Exception as e:
        await bot.reply_to(
            message,
            (
                "Invalid time declaration. "
                "Pass human readable time. "
                "(example: \"1s 1m 1h 1d 1w 1M 1y\")"
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
    """Ban user
    Args:
        message (types.Message): Message sent by the user.
        user_to_ban (types.User): User to ban.
        duration (int): Ban duration (in seconds)
        bot (AsyncTeleBot): Instance of a bot"""

    log.info(
        "Banning %d... Duration: %d" % (
            user_to_ban.id,
            duration
        )
    )
    unban_time = time.time() + duration

    await bot.ban_chat_member(
        message.chat.id,
        user_to_ban.id,
        until_date=unban_time
    )

    await bot.reply_to(
        message,
        "Banned <b>%s</b> (ID: <code>%d</code>) (Duration: %s)" % (
            user_to_ban.first_name,
            user_to_ban.id,

            # "If user is banned for more than 366 days or
            # less than 30 seconds from the current time
            # they are considered to be banned forever."
            # - https://core.telegram.org/bots/api#banchatmember
            str(datetime.timedelta(seconds=duration))
            if not duration < 30 and not duration > 31622400
            else "Forever"
        )
    )


async def _kick_user(
    message: types.Message,
    user_to_kick: types.User,
    bot: AsyncTeleBot
) -> None:
    """Ban user
    Args:
        message (types.Message): Message sent by the user.
        user_to_kick (types.User): User to kick.
        bot (AsyncTeleBot): Instance of a bot"""

    log.info("Kicking %s..." % user_to_kick.id)

    await bot.kick_chat_member(
        message.chat.id,
        user_to_kick.id
    )

    await bot.reply_to(
        message,
        "Kicked <b>%s</b> (ID: <code>%d</code>)" % (
            user_to_kick.first_name,
            user_to_kick.id
        )
    )


async def _mute_user(
    message: types.Message,
    user_to_mute: types.User,
    duration: int,
    bot: AsyncTeleBot
) -> None:
    """Mute user
    Args:
        message (types.Message): Message sent by the user.
        user_to_mute (types.User): User to mute.
        duration (int): mute duration (in seconds)
        bot (AsyncTeleBot): Instance of a bot"""

    log.info(
        "Muting %d... Duration: %d" % (
            user_to_mute.id,
            duration
        )
    )
    unmute_time = time.time() + duration

    await bot.restrict_chat_member(
        message.chat.id,
        user_to_mute.id,
        until_date=unmute_time
    )

    await bot.reply_to(
        message,
        "Muted <b>%s</b> (ID: <code>%d</code>) (Duration: %s)" % (
            user_to_mute.first_name,
            user_to_mute.id,

            # "If user is restricted for more than 366 days or
            # less than 30 seconds from the current time,
            # they are considered to be restricted forever"
            # - https://core.telegram.org/bots/api#restrictchatmember
            str(datetime.timedelta(seconds=duration))
            if not duration < 30 and not duration > 31622400
            else "Forever"
        )
    )


async def ban_handler(
    message: types.Message,
    bot: AsyncTeleBot
) -> None:
    """Handler for /ban command

    Args:
        message (types.Message): Message sent by the user.
        bot (AsyncTeleBot): Instance of a bot."""

    message_splitted = message.text.split()

    if not await _is_admin(message, bot):
        await bot.reply_to(message, "Not an admin.")
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
        except ValueError:
            await bot.reply_to(message, "Id must be an integer")
            return

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


async def kick_handler(
    message: types.Message,
    bot: AsyncTeleBot
) -> None:
    """Handler for /kick command

    Args:
        message (types.Message): Message sent by the user.
        bot (AsyncTeleBot): Instance of a bot."""

    if not await _is_admin(message, bot):
        await bot.reply_to(message, "Not an admin.")
        return

    if message.reply_to_message:
        user_to_kick = message.reply_to_message.from_user
        await _kick_user(
            message,
            user_to_kick,
            bot
        )
    elif len(message.text.split()) >= 2:
        message_splitted = message.text.split()
        try:
            user_to_kick_id = int(message_splitted[1])
        except ValueError:
            await bot.reply_to(message, "Id must be an integer")
            return

        member_to_kick = await bot.get_chat_member(
            message.chat.id,
            user_to_kick_id
        )
        await _kick_user(
            message,
            member_to_kick.user,
            bot
        )


async def mute_handler(
    message: types.Message,
    bot: AsyncTeleBot
) -> None:
    """Handler for /mute command

    Args:
        message (types.Message): Message sent by the user.
        bot (AsyncTeleBot): Instance of a bot."""

    message_splitted = message.text.split()

    if not await _is_admin(message, bot):
        await bot.reply_to(message, "Not an admin.")
        return

    if message.reply_to_message:
        user_to_mute = message.reply_to_message.from_user

        if len(message_splitted) > 1:
            duration = await _get_ban_duration(
                message,
                message_splitted[1:],
                bot
            )
        else:
            duration = 0

        await _mute_user(
            message,
            user_to_mute,
            duration,
            bot
        )
    elif len(message_splitted) > 1:
        if len(message_splitted) > 2:
            duration = await _get_ban_duration(
                message,
                message_splitted[2:],
                bot
            )
        else:
            duration = 0

        try:
            user_to_mute_id = int(message_splitted[1])
        except ValueError:
            await bot.reply_to(message, "Id must be an integer")
            return

        member_to_mute = await bot.get_chat_member(
            message.chat.id,
            user_to_mute_id
        )
        await _mute_user(
            message,
            member_to_mute.user,
            duration,
            bot
        )


async def id_handler(
    message: types.Message,
    bot: AsyncTeleBot
) -> None:
    """Handler for /id command

    Args:
        message (types.Message): Message sent by the user.
        bot (AsyncTeleBot): Instance of a bot."""

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        await bot.reply_to(
            message,
            "ID: <code>%i</code>" % user.id
        )
    else:
        await bot.reply_to(
            message,
            (
                "Reply to messages with this "
                "command to get the user ID."
            )
        )


__all__ = [
    "ban_handler",
    "kick_handler",
    "mute_handler",
    "id_handler"
]

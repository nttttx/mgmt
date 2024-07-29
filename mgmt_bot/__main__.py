import logging

from .bot import bot_main

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | [%(levelname)-8s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
    filename="app.log",
)

bot_main()

from .bot import bot_main
import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s in %(name)s - %(message)s",
    filename='app.log'
)

bot_main()

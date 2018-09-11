import logging

from discord.ext.commands import Bot, when_mentioned_or

from bot.constants import Bot as BotConfig


log = logging.getLogger(__name__)

bot = Bot(
    command_prefix=when_mentioned_or("!"),
    case_insensitive=True
)


bot.load_extension("bot.cogs.security")
bot.load_extension("bot.cogs.verification")

del bot.all_commands["help"]

bot.run(BotConfig.token)

import logging

from discord import Message, NotFound, Object
from discord.ext.commands import Bot, Context, command

from bot.constants import Channels, Roles
from bot.decorators import in_channel, without_role


log = logging.getLogger(__name__)


class Verification:
    """
    User verification
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    async def on_message(self, message: Message):
        if message.author.bot:
            return  # They're a bot, ignore

        ctx = await self.bot.get_context(message)  # type: Context

        if ctx.command is not None and ctx.command.name == "accept":
            return  # They used the accept command

        if ctx.channel.id == Channels.verification:  # We're in the verification channel
            for role in ctx.author.roles:
                if role.id == Roles.verified:
                    log.warning(f"{ctx.author} posted '{ctx.message.content}' "
                                "in the verification channel, but is already verified.")
                    return  # They're already verified

            log.trace(f"{ctx.author} posted '{ctx.message.content}' in the verification "
                      "channel - deleting it.")

            try:
                await ctx.message.delete()
            except NotFound:
                log.trace("No message found, it must have been deleted by another bot.")

    @command(name="accept", hidden=True, aliases=["verify", "verified", "accepted", "accept()"])
    @without_role(Roles.verified)
    @in_channel(Channels.verification)
    async def accept(self, ctx: Context, *_):  # We don't actually care about the args
        """
        Accept our rules and gain access to the rest of the server
        """

        log.debug(f"{ctx.author} called self.accept(). Assigning the user 'Developer' role.")
        await ctx.author.add_roles(Object(Roles.verified), reason="Accepted the rules")

        log.trace(f"Deleting the message posted by {ctx.author}.")

        try:
            await ctx.message.delete()
        except NotFound:
            log.trace("No message found, it must have been deleted by another bot.")


def setup(bot):
    bot.add_cog(Verification(bot))
    log.info("Cog loaded: Verification")

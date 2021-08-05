from discord.ext import commands
from discord_slash import SlashCommand


# cog.py
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def acommand(self, ctx, argument):
        await ctx.send("Stuff")

    @cog_ext.cog_slash(name="testimport",  guild_ids=[766312539994456105])
    async def _testping(ctx):  # Defines a new "context" (ctx) command called "ping."
        await ctx.send(f"Pong! ({bot.latency*1000}ms)")


def setup(bot):
    bot.add_cog(Slash(bot))

import discord
from discord.ext import commands

class VerificationInfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.content.lower() == "verifikace":
            await message.channel.send(
                "Pro verifikaci použij příkaz `/verify` s tvým školním emailem.\n"
                "Například: `/verify email: v1234a5@vfu.cz`"
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(VerificationInfoCog(bot))
import discord
from discord.ext import commands
from discord import app_commands
from loguru import logger

class VerifyTmpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="host", description="Verifikuj se jako host!")
    @app_commands.describe(heslo="Heslo které vám bylo zděleno :)")
    async def host(self, interaction: discord.Interaction, heslo: str):
        logger.info(f"Running host command with password: {heslo}")

        passp = "ainajetop"

        if heslo != passp:
            await interaction.response.send_message("Heslo není správné :(", ephemeral=True)
            return

        studentrole_host = discord.utils.get(interaction.guild.roles, name="pre-student")
        studentrole = discord.utils.get(interaction.guild.roles, name="👨‍⚕️ Student")

        if studentrole_host is None or studentrole is None:
            await interaction.response.send_message("Role not found.", ephemeral=True)
            return
            
        await interaction.user.add_roles(studentrole)
        await interaction.user.add_roles(studentrole_host)

        logger.info(f"New host user {interaction.user}")

        await interaction.user.send("Gratulace! Vítej mezi námi")
        await interaction.response.send_message("Gratulace! Vítej mezi námi", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(VerifyTmpCog(bot))
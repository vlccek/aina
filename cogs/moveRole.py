import discord
from discord.ext import commands
from discord import app_commands
from loguru import logger

class MoveRoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="increment_year", description="Increments the roles and permissions for a new school year.")
    @app_commands.checks.has_permissions(administrator=True)
    async def increment_year(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        role_names = [
            "1. Australopithecus",
            "2. Homo habilis",
            "3. Homo erectus",
            "4. Homo neanderthalensis",
            "5. Homo sapiens",
            "6. Homo sapiens veterinariens",
            "Vet",
        ]

        roles = [discord.utils.get(guild.roles, name=role_name) for role_name in role_names]
        
        if any(role is None for role in roles):
            await interaction.response.send_message("One or more roles not found.", ephemeral=True)
            return

        role_colors = [role.color for role in roles]

        await interaction.response.defer(ephemeral=True)

        try:
            for i in range(5):
                await roles[i].edit(name=role_names[i + 1], color=role_colors[i + 1])

            australopithecus = await guild.create_role(name=role_names[0], color=role_colors[0])
            
            for member in roles[5].members:
                await member.add_roles(roles[6])

            await roles[5].delete()

            logger.info("Roles incremented successfully.")

            category_names = [
                "📕 1. ROČNÍK - ZIMNÍ SEMESTR",
                "📕 1. ročník - letní semestr",
                "📗 2. ročník - zimní semestr",
                "📗 2. ROČNÍK - letní semestr",
                "📘 3. ročník - ZIMNÍ SEMESTR",
                "📘 3. ročník - LETNÍ SEMESTR",
                "📙 4. ročník - zimní semestr",
                "📙 4. ročník - letní semestr",
                "📔5. ročník - zimní semestr",
                "📔5. ročník - letní semestr",
            ]

            categories = [discord.utils.get(guild.categories, name=name_cat) for name_cat in category_names]

            if any(category is None for category in categories):
                await interaction.followup.send("One or more categories not found.")
                return

            await categories[0].set_permissions(roles[0], read_messages=True)
            await categories[1].set_permissions(roles[0], read_messages=True)
            await categories[2].set_permissions(roles[1], read_messages=True)
            await categories[3].set_permissions(roles[1], read_messages=True)
            await categories[4].set_permissions(roles[2], read_messages=True)
            await categories[5].set_permissions(roles[2], read_messages=True)
            await categories[6].set_permissions(roles[3], read_messages=True)
            await categories[7].set_permissions(roles[3], read_messages=True)
            await categories[8].set_permissions(roles[4], read_messages=True)
            await categories[9].set_permissions(roles[4], read_messages=True)
            
            logger.info("Permissions updated successfully.")
            await interaction.followup.send("Year incremented successfully!")

        except Exception as e:
            logger.error(f"An error occurred during year increment: {e}")
            await interaction.followup.send(f"An error occurred: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(MoveRoleCog(bot))
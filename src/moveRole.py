import discord
from discord.ext import commands
from discord import app_commands
from loguru import logger
import sys 

sys.path.append("/app")
from settings import guild_ids

class Aina(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="incpart1", description="Increment roles - Part 1")
    async def increment_roles_part1(self, interaction: discord.Interaction):
        guild = interaction.guild

        roleNames = [
            "1. Australopithecus",
            "2. Homo habilis",
            "3. Homo erectus",
            "4. Homo neanderthalensis",
            "5. Homo sapiens",
            "6. Homo sapiens veterinariens",
            "Vet",
        ]

        roles = [discord.utils.get(guild.roles, name=roleName) for roleName in roleNames]
        roles_colors = [role.color for role in roles]

        for i in range(0, 5):
            await roles[i].edit(name=roleNames[i + 1], color=roles_colors[i + 1])

        Australopithecus = await guild.create_role(name=roleNames[0], color=roles_colors[0])

        for member in roles[5].members:
            await member.add_roles(roles[6])

        await roles[5].delete()

        await interaction.response.send_message("Holy fuck, role jsou ok tedka se jde na práva :() ")

        roles_names = [
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
            "7",
            "8",
        ]

        categories = [discord.utils.get(guild.categories, name=name_cat) for name_cat in roles_names]

        for i in range(6):
            await categories[i*2].set_permissions(roles[i], read_messages=True)
            await categories[i*2+1].set_permissions(roles[i], read_messages=True)

        await categories[8].set_permissions(roles[4], read_messages=True)
        await categories[9].set_permissions(roles[4], read_messages=True)

    @app_commands.command(name="incpart2", description="Increment roles - Part 2")
    async def increment_roles_part2(self, interaction: discord.Interaction):
        guild = interaction.guild
        roleNames = [
            "1. Australopithecus",
            "2. Homo habilis",
            "3. Homo erectus",
            "4. Homo neanderthalensis",
            "5. Homo sapiens",
            "6. Homo sapiens veterinariens",
            "Vet",
        ]

        roles_names = [
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
            "7",
            "8",
        ]

        roles = [discord.utils.get(guild.roles, name=roleName) for roleName in roleNames]
        categories = [discord.utils.get(guild.categories, name=name_cat) for name_cat in roles_names]

        for i in range(5):
            await categories[i*2].set_permissions(roles[i], read_messages=True)
            await categories[i*2+1].set_permissions(roles[i], read_messages=True)

        await interaction.response.send_message("Permissions updated successfully.")

async def setup(bot):
    await bot.add_cog(Aina(bot))        
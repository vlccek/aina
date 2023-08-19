import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from loguru import logger
import sys 


sys.path.append("/app")
from settings import guild_ids



class Aina(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="inc", guild_ids=guild_ids)
    async def increment_roles(self, ctx):
        guild = ctx.guild

        roleNames = [
            "1. Australopithecus",
            "2. Homo habilis",
            "3. Homo erectus",
            "4. Homo neanderthalensis",
            "5. Homo sapiens",
            "6. Homo sapiens veterinariens",
            "Vet",
        ]

        roles = [
            discord.utils.get(guild.roles, name=roleName) for roleName in roleNames
        ]
        #  uložím si konrétní role do seznamu 0 jsou obratlovci

        roles_colors = [role.color for role in roles]
        # uložím si colory co měli role předtím

        for i in range(0, 5):
            await roles[i].edit(name=roleNames[i + 1], color=roles_colors[i + 1])

        Australopithecus = await guild.create_role(
            name=roleNames[0], color=roles_colors[0]
        )
        #  await Australopithecus.edit(position=roles[0].position - 1)
        # vytvořím nové obratlovce (nové prváky)

        for member in roles[5].members:
            await member.add_roles(roles[6])
            # přehodím absolventy

        await roles[5].delete()

        # await discord.utils.get(guild.roles, name=roleNames[5]).delete()

        await ctx.send("Holy fuck, role jsou ok tedka se jde na práva :() ")

        roles_names = [
            "📕 1. ROČNÍK - ZIMNÍ SEMESTR",
            "📕 1. ročník - letní semestr",
            "📗 2. ročník - zimní semestr",
            "📗 2. ROČNÍK - letní semestr",
            "📘 3. ročník - ZIMNÍ SEMESTR",
            "📘 3. ročník - LETNÍ SEMESTR",
            "📙 4. ročník - zimní semestr",
            "📙 4. ročník - letní semestr",
            "5. ročník - zimní semestr",
            "5. ročník - letní semestr",
            "7",
            "8",
        ]

        roles = [
            discord.utils.get(guild.roles, name=roleName) for roleName in roleNames
        ]

        categories = [
            discord.utils.get(guild.categories, name=name_cat)
            for name_cat in roles_names
        ]

        await categories[0].set_permissions(roles[0], read_messages=True)
        await categories[1].set_permissions(roles[0], read_messages=True)

        await categories[2].set_permissions(roles[1], read_messages=True)
        await categories[3].set_permissions(roles[1], read_messages=True)

        await categories[4].set_permissions(roles[2], read_messages=True)
        await categories[5].set_permissions(roles[2], read_messages=True)

        # await categories[6].set_permissions(roles[3], read_messages=True)
        # await categories[7].set_permissions(roles[3], read_messages=True)

        await categories[8].set_permissions(roles[4], read_messages=True)
        await categories[9].set_permissions(roles[4], read_messages=True)



    @cog_ext.cog_slash(name="incpart2", guild_ids=guild_ids)
    async def increment_roles(self, ctx):
        guild = ctx.guild
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

        roles = [
            discord.utils.get(guild.roles, name=roleName) for roleName in roleNames
        ]

        categories = [
            discord.utils.get(guild.categories, name=name_cat)
            for name_cat in roles_names
        ]

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


def setup(bot):
    bot.add_cog(Aina(bot))


import discord
# Importing the newly installed library.
from discord_slash import SlashCommand
from discord_slash import cog_ext
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option
from src.database.crud import initTable

import os
import settings

loaded_modules = list()


def load_extension(name):
    loaded_modules.append(name)
    print(name)
    bot.load_extension(name)


bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot,
                     sync_commands=True,
                     sync_on_cog_reload=True,
                     override_type=True)
guild_ids = [766312539994456105]
bot.db = initTable()


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@slash.slash(name="ping", guild_ids=guild_ids)
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")


@slash.slash(
    name="load_module",
    description="načte modul",
    options=[
        create_option(
            name="modul",
            description="modulu který chceš načíst",
            option_type=3,
            required=True,
        )
    ],
    guild_ids=guild_ids,
)
async def load_module(ctx, modul: str):
    load_extension(modul)


@slash.slash(name='loaded_modules', description="Vypíše načtené moduly bro")
def _loaded_modules(ctx):
    ctx.send(loaded_modules)


load_extension("src.test")
load_extension("src.tictactoe")
bot.run(settings.token)

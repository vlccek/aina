import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings

# Load environment variables
load_dotenv()

# Database setup

from src.database.crud import initTable
DATABASE_URL = settings.DATABASE_URL
engine = initTable()
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Add database session to bot
bot.engine = AsyncSessionLocal


# Automatic cog loading
async def load_extensions():
    for filename in os.listdir('./src'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'src.{filename[:-3]}')
                print(f'Loaded extension: {filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename[:-3]}:', str(e))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.load_extension(f'src.verify')
    # await bot.load_extension(f'src.moveRole')

    await bot.tree.sync()
    print("Bot is ready!")

@bot.tree.command(name="load", description="Load a command module")
@commands.has_permissions(administrator=True)
async def load(interaction: discord.Interaction, module: str):
    try:
        await bot.load_extension(f'cogs.{module}')
        await bot.tree.sync()
        await interaction.response.send_message(f"Module {module} loaded successfully!")
    except Exception as e:
        await interaction.response.send_message(f"Failed to load module {module}: {str(e)}")

@bot.tree.command(name="unload", description="Unload a command module")
@commands.has_permissions(administrator=True)
async def unload(interaction: discord.Interaction, module: str):
    try:
        await bot.unload_extension(f'cogs.{module}')
        await bot.tree.sync()
        await interaction.response.send_message(f"Module {module} unloaded successfully!")
    except Exception as e:
        await interaction.response.send_message(f"Failed to unload module {module}: {str(e)}")

@bot.tree.command(name="reload", description="Reload a command module")
@commands.has_permissions(administrator=True)
async def reload(interaction: discord.Interaction, module: str):
    try:
        await bot.reload_extension(f'cogs.{module}')
        await bot.tree.sync()
        await interaction.response.send_message(f"Module {module} reloaded successfully!")
    except Exception as e:
        await interaction.response.send_message(f"Failed to reload module {module}: {str(e)}")

@bot.command()
@commands.is_owner()
async def sync(ctx, guild_id: int = None):
    if guild_id:
        guild = discord.Object(id=guild_id)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        await ctx.send(f"Slash commands synced to guild {guild_id}")
    else:
        await bot.tree.sync()
        await ctx.send("Global slash commands synced")

@bot.command()
@commands.is_owner()
async def sync_all(ctx):
    synced = await bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} commands globally")
    for guild in bot.guilds:
        try:
            await bot.tree.sync(guild=guild)
            await ctx.send(f"Synced commands for guild: {guild.name} ({guild.id})")
        except Exception as e:
            await ctx.send(f"Failed to sync commands for guild {guild.name}: {str(e)}")

# Run the bot
bot.run(settings.token)
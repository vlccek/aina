import discord
from discord.ext import commands
from loguru import logger
import os
import asyncio

from config import settings

class AinaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=".", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    logger.info(f"Loaded extension: {filename}")
                except Exception as e:
                    logger.error(f"Failed to load extension {filename}: {e}")
        
        if settings.GUILD_IDS:
            for guild_id in settings.GUILD_IDS:
                guild = discord.Object(id=guild_id)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def on_ready(self):
        logger.info(f"{self.user.name} has connected to Discord!")
        logger.info(f"Aina starts succesfull. Logged by {self.user.name}. Id of aina {self.user.id}. ")


async def main():
    bot = AinaBot()
    await bot.start(settings.TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import re
from loguru import logger
import datetime

# cog.py
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

import src.database.models as dbTypes

import smtplib, ssl
from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from src.database.models import registrationUser, User
from sqlalchemy.sql import select
import sys

sys.path.append("/app")
from settings import guild_ids, email_pass, email_name


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="host",
        description="Verifikuj se!",
        options=[
            create_option(
                name="heslo",
                description="Heslo které vám bylo zděleno :)",
                option_type=3,
                required=True,
            )
        ],
        guild_ids=guild_ids,
    )
    async def slash_host(self, ctx, heslo):
        ctx.defer()
        logger.info("Runing host command with")

        passp = "ainajetop"
        passp2 = "jsemprvak"

        if heslo != passp or heslo != passp2:
            await ctx.send(
                "Heslo není správné :(",
                delete_after=10,
            )
            return

        if heslo == passp2:
            name = "skoroprvak"
        else:
            name = "pre-student"


        studentrole_host = discord.utils.get(ctx.guild.roles, name=name)
        studentrole = discord.utils.get(ctx.guild.roles, name="👨‍⚕️ Student")
        await ctx.author.add_roles(studentrole)
        await ctx.author.add_roles(studentrole_host)

        logger.info(f"New host user {ctx.author}")

        await ctx.author.send("Gratulace! Vítej mezi námi")
        await ctx.send(
            "Gratulace! Vítej mezi námi",
            delete_after=10,
        )


def setup(bot):
    bot.add_cog(Slash(bot))

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
        logger.info("Runing host command with")

        passp = "ainajetop"

        if heslo != passp:
            await ctx.send(
                "Heslo není správné :(",
                delete_after=10,
            )
            return

        studentrole = discord.utils.get(ctx.guild.roles, name="pre-student")
        await ctx.author.add_roles(studentrole)

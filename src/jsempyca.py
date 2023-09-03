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
        name="fixpeople",
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
    async def slash_pyca(self, ctx, heslo):
        ctx.defer()
        logger.info("Runing host command with")

        people= [
                687717081898156079,
                784538116890427392,
                1136055972964618270,
                1145475116755587083,
                1134531376650145873,
                767296837073764412,
                886850972578631740,
                886850972578631740,
                718040247589666876,
                1147435433958068235,
                1147435433958068235,
                762705025478688818,
                1147490807373365340,
                687008009029025799,
                687008009029025799,
                685594332916613210,
                770915147002019861,
                695575378391072870,
                1147440283584303115,
                439316316307062784,
        ]

        studentrole = discord.utils.get(ctx.guild.roles, name="👨‍⚕️ Student")
        ve = discord.utils.get(ctx.guild.roles, name="Veterinární lekářství")
        be = discord.utils.get(ctx.guild.roles, name="Veterinární hygiena a ekologie")



        for i in people:
            ctx.message.server.get_member(i)
            ctx.author.remove_roles(studentrole)  
            ctx.author.remove_roles(ve)   
            ctx.author.remove_roles(be)   



        await ctx.send(
            "Bohužel jsem u tebe zjistil chybu při registraci. Opravou je že ti byla odebrána role. POkud máš stále zájem být součastí komuniky VETUNI se prosím znovu registruj. Na tuto zprávu neodpovídej byla poslána robotem.",
            delete_after=10,
        )


def setup(bot):
    bot.add_cog(Slash(bot))

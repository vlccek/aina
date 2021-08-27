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

from src.database.models import  registrationUser, User 
from sqlalchemy.sql import select


def parseMail(message):
    reemail = re.search("^(([vh])((\d{2})\d{3})\@vfu\.cz)$", message)
    return reemail


def send_mail_to(nameofuser: str, receiver: str, token : str):
    logger.info(f"Sending mail to address {receiver} with token {token} name of user are {nameofuser}")
    context = ssl.create_default_context()
    smtp_server = "smtp.seznam.cz"
    port = 465  # For starttls
    sender_email = "aina@jevlk.cz"
    password = "ainajenej123"
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Tvůj ověřovací kód pro Discord server VetUni"
        msg["From"] = "Aina BOT <aina@jevlk.cz>"
        msg["To"] = receiver
        msg["Date"] = formatdate()

        # Create the body of the message (a plain-text and an HTML version).
        text = "Ahoj {0}, tvůj ověřovací kód je:\n/kod kod: {1}\nZadej ho v kanále #komunikace-s-botem.".format(
            nameofuser, token
        )
        html = """\
        <html>
        <head></head>
        <body>
            <p>Ahoj {0},<br>
            tvůj ověřovací kód je: <b>{1}</b><br>Zadej ho v kanále #komunikace-s-botem.
            Pokud nevíš, o co se jedná, tak můžeš tento email směle ignovat :D
        </body>
        </html>
        """.format(
            nameofuser, token
        )

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        server.sendmail(sender_email, receiver, msg.as_string())

    return token


def generatetoken():
    rand_token = uuid4()
    return "t{0}".format(rand_token)


def check_mail_vfu(email):
    regex = "^[vh]\d{5}\@vfu\.cz$"
    if re.search(regex, email):
        return True
    else:
        return False


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="verify",
        description="Verifikuj se!",
        options=[
        create_option(
            name="email",
            description="Email z vfu",
            option_type=3,
            required=True,
        )
    ],
        guild_ids=bot.guild_ids,
    )
    async def slash_verify(self, ctx, email):
        logger.info("Runing verify command with")
        if check_mail_vfu(email):
            await ctx.send(
                "Haf, velmi brzy ti dorazí email. Zbytek instrukcí je v mailu. Pokud nepřijde do pěti minut, zkus zkontrolovat nevyžádanou poštu nebo kontaktuj správce.",
                delete_after=10,
            )
            token = generatetoken()
            send_mail_to(ctx.author.name, email, token)
            newuser = registrationUser(idofuser=ctx.author.id, email=email,dateOfMailSend=datetime.datetime.now(),token=token , nameofuser=ctx.author.name)
            self.bot.db.add(newuser)
            self.bot.db.commit()
        else:
            await ctx.send(
                "Text který si zadal neodpovídá mail z VFU. Pro registraci je potřeba jedině školní mail",
                delete_after=10,
            )
    
    @cog_ext.cog_slash(
        name="kod",
        description="Verifikuj se!",
        options=[
        create_option(
            name="kod",
            description="Email z vfu",
            option_type=3,
            required=True,
        )
    ],
        guild_ids=bot.guild_ids,
    )
    async def slash_kod(self, ctx, kod):
        logger.info(f"User: {ctx.author.name} with id: {ctx.author.id}. Are trying to use command /kod with token {kod}")
        result = self.bot.db.query(registrationUser).filter_by(token=kod).first()
        
        if not result.idofuser == ctx.author.id:
            await ctx.send("Tento token nenáležík tvému učtu")

        parsedMail = parseMail(result.email)

        studentrole = discord.utils.get(ctx.guild.roles, name="👨‍⚕️ Student")
        await ctx.author.add_roles(studentrole)

        if parsedMail.group(2) == "v":
            faculty = "Veterinární lekářství"
            facultyrole = discord.utils.get(
                ctx.guild.roles, name="Veterinární lekářství"
            )
            await ctx.author.add_roles(facultyrole)
        elif parsedMail.group(2) == "h":
            faculty = "Veterinární hygiena a ekologie"
            facultyrole = discord.utils.get(
                ctx.guild.roles, name="Veterinární hygiena a ekologie"
            )
            await ctx.author.add_roles(facultyrole)
        else:
            faculty = "Unkown"
            await ctx.author.add_roles(facultyrole)

        grade = parsedMail.group(4)

        newUser = User(idx= ctx.author.id, email=result.email, dateOfMailSend=result.dateOfMailSend, dateOfaddingRoles=datetime.datetime.now(), grade=grade, faculty=faculty)
        self.bot.db.add(newUser)
        self.bot.db.commit()
        await ctx.send("Byl jsi uspěšně verifikován!", delete_after=10)


        


def setup(bot):
    bot.add_cog(Slash(bot))

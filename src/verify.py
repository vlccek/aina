import discord
from discord import app_commands
from discord.ext import commands
import re
from loguru import logger
import datetime
import smtplib
import ssl
from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, selectinload

import sys
sys.path.append("/app")
from settings import guild_ids, email_pass, email_name, DATABASE_URL
from src.database.models import registrationUser, User

# ... [previous functions remain the same] ...

def generate_token():
    return f"t{uuid4()}"

def parse_mail(message):
    return re.search(r"^([vh])(\d{5})@vfu\.cz$", message)

def send_mail_to(nameofuser: str, receiver: str, token: str):
    logger.info(f"Sending mail to address {receiver} with token {token} name of user are {nameofuser}")
    context = ssl.create_default_context()
    smtp_server = "smtp.seznam.cz"
    port = 465
    sender_email = email_name
    password = email_pass

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Tvůj ověřovací kód pro Discord server VetUni"
        msg["From"] = "Aina BOT <aina@jevlk.cz>"
        msg["To"] = receiver
        msg["Date"] = formatdate()

        text = f"Ahoj {nameofuser}, tvůj ověřovací kód je:\n/kod kod: {token}\nZadej ho v kanále #komunikace-s-botem."
        html = f"""
        <html>
        <body>
            <p>Ahoj {nameofuser},<br>
            tvůj ověřovací kód je: <b>{token}</b><br>Zadej ho v kanále #komunikace-s-botem.
            Pokud nevíš, o co se jedná, tak můžeš tento email směle ignovat :D
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        server.sendmail(sender_email, receiver, msg.as_string())

    return token

def generate_token():
    return f"t{uuid4()}"


def check_mail_vfu(email):
    return bool(re.match(r"^[vh]\d{5}@vfu\.cz$", email))


class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    @app_commands.command(name="verify", description="Verifikuj se!")
    @app_commands.describe(email="Email z VFU")
    async def verify(self, interaction: discord.Interaction, email: str):
        logger.info(f"Running verify command for {interaction.user.name}")

        session = self.Session()
        
        if session.query(User).filter_by(idx=interaction.user.id).first():
            await interaction.response.send_message(
                "Už si verifikován. Pokud nevidíš kanály, obrať se na Správce.",
                ephemeral=True
            )
            session.close()
            return

        if check_mail_vfu(email):
            await interaction.response.send_message(
                "Haf, velmi brzy ti dorazí email. Zbytek instrukcí je v mailu. Pokud nepřijde do pěti minut, zkus zkontrolovat nevyžádanou poštu nebo kontaktuj správce.",
                ephemeral=True
            )
            token = generate_token()
            send_mail_to(interaction.user.name, email, token)
            newuser = registrationUser(
                idofuser=interaction.user.id,
                email=email,
                dateOfMailSend=datetime.datetime.now(),
                token=token,
                nameofuser=interaction.user.name,
            )
            session.add(newuser)
            session.commit()
        else:
            await interaction.response.send_message(
                "Text který jsi zadal neodpovídá mailu z VFU. Pro registraci je potřeba jedině školní mail.",
                ephemeral=True
            )
        session.close()

    @app_commands.command(name="kod", description="Verifikuj se pomocí kódu!")
    @app_commands.describe(kod="Verifikační kód z emailu")
    async def kod(self, interaction: discord.Interaction, kod: str):
        logger.info(f"User: '{interaction.user.name}' with id: '{interaction.user.id}' is trying to use command /kod with token '{kod}'")

        session = self.Session()

        registration = session.query(registrationUser).filter(registrationUser.token == kod).first()

        if not registration:
            await interaction.response.send_message(
                "Takový kód není v databázi. Pravděpodobně jsi jej špatně zkopíroval. Pokud bude problém nadále přetrvávat, kontaktuj správce.",
                ephemeral=True
            )
            session.close()
            return

        if registration.idofuser != interaction.user.id:
            await interaction.response.send_message("Tento token nenáleží k tvému účtu", ephemeral=True)
            session.close()
            return

        parsed_mail = parse_mail(registration.email)
        if not parsed_mail:
            await interaction.response.send_message("Neplatný email v databázi. Kontaktuj správce.", ephemeral=True)
            session.close()
            return

        student_role = discord.utils.get(interaction.guild.roles, name="👨‍⚕️ Student")
        await interaction.user.add_roles(student_role)

        faculty = "Veterinární lekářství" if parsed_mail.group(1) == "v" else "Veterinární hygiena a ekologie"
        faculty_role = discord.utils.get(interaction.guild.roles, name=faculty)
        await interaction.user.add_roles(faculty_role)

        grade = parsed_mail.group(2)[:2]
        today = datetime.date.today()
        year = today.year - (1 if today.month < 9 else 0)
        study_year = (year % 2000) - int(grade)

        role_names = [
            "1. Australopithecus",
            "2. Homo habilis",
            "3. Homo erectus",
            "4. Homo neanderthalensis",
            "5. Homo sapiens",
            "6. Homo sapiens veterinariens",
            "Vet",
        ]
        year_role = discord.utils.get(interaction.guild.roles, name=role_names[min(study_year, 6)])
        await interaction.user.add_roles(year_role)

        new_user = User(
            idx=interaction.user.id,
            email=registration.email,
            dateOfMailSend=registration.dateOfMailSend,
            dateOfaddingRoles=datetime.datetime.now(),
            grade=grade,
            faculty=faculty,
        )
        session.add(new_user)
        session.commit()
        session.close()

        await interaction.user.send("Gratulace! Vítej na serveru VET-UNI")
        await interaction.response.send_message("Byl jsi úspěšně verifikován!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(VerificationCog(bot))
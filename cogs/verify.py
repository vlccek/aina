import discord
from discord.ext import commands
from discord import app_commands
import re
from loguru import logger
import datetime
import hmac
import hashlib
from typing import Optional, Tuple

from utils.email_sender import send_verification_email, send_registration_email
from config import settings

def generate_token(user_id: int, faculty: str, grade: str) -> str:
    hash_part = hmac.new(
        settings.SECRET_KEY.encode(),
        str(user_id).encode(),
        hashlib.sha256
    ).hexdigest()[:6]
    return f"{hash_part}_{grade}{faculty}"

def check_mail_vfu(email):
    regex = r"^[vh](\d{2})\d{3}\@vfu\.cz$"
    return re.search(regex, email)

class VerifyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="verify", description="Verifikuj se!")
    @app_commands.describe(email="Email z vfu")
    async def verify(self, interaction: discord.Interaction, email: str):
        logger.info(f"Running verify command with {email}")

        parsed_mail = check_mail_vfu(email)
        is_test_email = email.endswith("@jevlk.cz")

        if parsed_mail or is_test_email:
            await interaction.response.send_message(
                "Haf, velmi brzy ti dorazí email. Zbytek instrukcí je v mailu. Pokud nepřijde do pěti minut, zkus zkontrolovat nevyžádanou poštu nebo kontaktuj správce.",
                ephemeral=True,
            )
            if is_test_email:
                faculty = "t"
                grade = "es"
            else:
                faculty = parsed_mail.group(0)[0]
                grade = parsed_mail.group(1)

            token = generate_token(interaction.user.id, faculty, grade)
            send_verification_email(interaction.user.name, email, token)
        else:
            await interaction.response.send_message(
                "Text který si zadal neodpovídá mail z VFU. Pro registraci je potřeba jedině školní mail",
                ephemeral=True,
            )

    @app_commands.command(name="kod", description="Zadej kód z emailu")
    @app_commands.describe(kod="Kód z emailu")
    async def kod(self, interaction: discord.Interaction, kod: str):
        await interaction.response.defer(ephemeral=True)
        logger.info(
            f"User: '{interaction.user.name}' with id: '{interaction.user.id}'. Are trying to use command /kod with token '{kod}'"
        )
        
        try:
            hash_part, data_part = kod.split('_')
            grade = data_part[:-1]
            faculty = data_part[-1]
            logger.info(f"Parsed grade: '{grade}' and faculty: '{faculty}'")

        except ValueError:
            await interaction.followup.send(
                "Neplatný formát tokenu.",
                ephemeral=True,
            )
            return

        expected_hash_part = hmac.new(
            settings.SECRET_KEY.encode(),
            str(interaction.user.id).encode(),
            hashlib.sha256
        ).hexdigest()[:6]

        logger.info(f"Expected hash is {expected_hash_part}")

        if not hmac.compare_digest(expected_hash_part, hash_part):
            logger.warning(
                f"User: '{interaction.user.name}' with id: '{interaction.user.id}'. Trying to use unknown or incorrect token."
            )
            await interaction.followup.send(
                "Takový kod není v databázi, nebo je neplatný. Pravděpodobně si jej špatně zkopíroval. Pokud bude problém nadále přetrvávat kontaktuj správce.",
                ephemeral=True,
            )
            return

        logger.success(f"User: '{interaction.user.name}' with id: '{interaction.user.id}' has been successfully verified.")

        added_roles = []

        if faculty == "t" and grade == "es": # test
            logger.info("Assigning test roles.")
            student_role = discord.utils.get(interaction.guild.roles, name="👨‍⚕️ Student")
            await interaction.user.add_roles(student_role)
            added_roles.append(student_role)
            logger.info(f"Added role '{student_role.name}' to user '{interaction.user.name}'")
            faculty_role = discord.utils.get(interaction.guild.roles, name="Veterinární lekářství")
            await interaction.user.add_roles(faculty_role)
            added_roles.append(faculty_role)
            logger.info(f"Added role '{faculty_role.name}' to user '{interaction.user.name}'")
            grade_role = discord.utils.get(interaction.guild.roles, name="1. Australopithecus")
            await interaction.user.add_roles(grade_role)
            added_roles.append(grade_role)
            logger.info(f"Added role '{grade_role.name}' to user '{interaction.user.name}'")
        else:
            student_role = discord.utils.get(interaction.guild.roles, name="👨‍⚕️ Student")
            await interaction.user.add_roles(student_role)
            added_roles.append(student_role)
            logger.info(f"Added role '{student_role.name}' to user '{interaction.user.name}'")

            if faculty == "v":
                faculty_name = "Veterinární lekářství"
                faculty_role = discord.utils.get(
                    interaction.guild.roles, name=faculty_name
                )
                await interaction.user.add_roles(faculty_role)
                added_roles.append(faculty_role)
                logger.info(f"Added role '{faculty_role.name}' to user '{interaction.user.name}'")
            elif faculty == "h":
                faculty_name = "Veterinární hygiena a ekologie"
                faculty_role = discord.utils.get(
                    interaction.guild.roles, name=faculty_name
                )
                await interaction.user.add_roles(faculty_role)
                added_roles.append(faculty_role)
                logger.info(f"Added role '{faculty_role.name}' to user '{interaction.user.name}'")

            roleNames = [
                "1. Australopithecus",
                "2. Homo habilis",
                "3. Homo erectus",
                "4. Homo neanderthalensis",
                "5. Homo sapiens",
                "6. Homo sapiens veterinariens",
                "Vet",
            ]

            today = datetime.date.today()
            year = today.year
            if today.month < 9:
                year -=1

            role_index = (int(grade) - year % 100) * -1
            logger.info(f"Calculated role_index: {role_index}")

            if 0 <= role_index < len(roleNames):
                grade_role = discord.utils.get(interaction.guild.roles, name=roleNames[role_index])
                await interaction.user.add_roles(grade_role)
                added_roles.append(grade_role)
                logger.info(f"Added role '{grade_role.name}' to user '{interaction.user.name}'")
            else:
                logger.warning(f"Role_index: '{role_index}' is out of range.")

        notification_user = await self.bot.fetch_user(268447808716144641)
        role_names = ", ".join([role.name for role in added_roles])
        await notification_user.send(f"New user verified: {interaction.user.name} ({interaction.user.id})\nRoles added: {role_names}\nToken used: {kod}")

        # send_registration_email(interaction.user)

        await interaction.followup.send("Gratulace! Vítej na serveru VET-UNI. Byl jsi uspěšně verifikován!", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(VerifyCog(bot))
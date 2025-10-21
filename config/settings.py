import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_IDS = [int(guild_id) for guild_id in os.getenv("GUILD_IDS", "").split(",")]
EMAIL_ADDRESS = "aina@jevlk.cz"
EMAIL_NAME = os.getenv("EMAIL_NAME")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SECRET_KEY = os.getenv("SECRET_KEY")
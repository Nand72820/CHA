from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = "29893020"
API_HASH = "28e79037f0b334ef0503466c53f08af5"
BOT_TOKEN = getenv("BOT_TOKEN", None)
STRING1 = getenv("STRING_SESSION", None)
MONGO_URL = getenv("MONGO_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 6399386263))
SUPPORT_GRP = "NYCreation_Chatzone"
UPDATE_CHNL = "CreativeYdv"
OWNER_USERNAME = "Yo_Mysterious"

from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = "22180072"
API_HASH = "425c7b0d42d9aa0f0b69c07687787175"
BOT_TOKEN = getenv("BOT_TOKEN", None)
STRING1 = getenv("STRING_SESSION", None)
MONGO_URL = getenv("MONGO_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 1786683163))
SUPPORT_GRP = "NYCreation_Chatzone"
UPDATE_CHNL = "CreativeYdv"
OWNER_USERNAME = "Yo_Mysterious"

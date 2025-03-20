import os

from dotenv import load_dotenv

load_dotenv()

DEVS = [
   
    ]
    
    
KYNAN = list(map(int, os.getenv("KYNAN", "").split()))

API_ID = int(os.getenv("API_ID", ""))

API_HASH = os.getenv("API_HASH", "")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

OWNER_ID = int(os.getenv("OWNER_ID", ""))

api_key = os.getenv("AKENO_KEY", "")

USER_ID = list(
    map(
        int,
        os.getenv(
            "USER_ID",
            "",
        ).split(),
    )
)

LOG_UBOT = int(os.getenv("LOG_UBOT", ""))

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1001608847572 -1001538826310 -1001876092598 -1001864253073 -1001451642443 -1001825363971 -1001797285258 -1001927904459 -1001287188817 -1001812143750 -1001608701614 -1001473548283 -1001861414061 -1002133716625",
        ).split(),
    )
)

MAX_BOT = int(os.getenv("MAX_BOT", "25"))

RMBG_API = os.getenv("RMBG_API", "")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "",
).split()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "",
)

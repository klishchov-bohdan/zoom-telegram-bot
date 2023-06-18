import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins_id = [
    656634975,
]

DBIP = os.getenv('DBIP')
PGUSER = str(os.getenv('PGUSER'))
PGPASS = str(os.getenv('PGPASS'))
DB = str(os.getenv('DB'))

ZOOM_ACCOUNT_ID = str(os.getenv('ZOOM_ACCOUNT_ID'))
ZOOM_CLIENT_ID = str(os.getenv('ZOOM_CLIENT_ID'))
ZOOM_CLIENT_SECRET = str(os.getenv('ZOOM_CLIENT_SECRET'))

GOOGLE_APP_PASS = str(os.getenv('GOOGLE_APP_PASS'))
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_SERVER = str(os.getenv('SMTP_SERVER'))

chat_id = -972603444

POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASS}@{DBIP}/{DB}'

banned_messages = ['qwerty', 'sss']

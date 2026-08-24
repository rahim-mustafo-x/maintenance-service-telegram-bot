from dotenv import load_dotenv
from os import getenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
ADMINS = [5953769207]
ADMIN_USER_NAME = getenv('ADMIN_USER_NAME')
PORT = int(getenv('PORT'))

def code_text(code:str) ->str:
    return f'Tasdiqlash kodi <code>{code}</code>\nUshbu kodni hech kimga bermang!'

def here_is_admin_user_name(username:str) -> str:
    return f'Siz bu holatni ushbu {username} ga yozishingiz mumkin'
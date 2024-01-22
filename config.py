from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.getcwd(), 'token.env'))

path_to_db = 'db.db'
TOKEN = os.environ['TOKEN']
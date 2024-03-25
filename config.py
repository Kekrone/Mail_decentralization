from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.getcwd(), '/root/bot//token.env'))

path_to_db = '/etc/postfix/virtuals.db'
TOKEN = os.environ['TOKEN']
pswd = os.environ['pswd']

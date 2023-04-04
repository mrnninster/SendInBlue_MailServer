import os
from dotenv import load_dotenv

load_dotenv('mail_app/.env')
app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
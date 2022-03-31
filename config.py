
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    NOTION_API_TOKEN = os.environ.get("NOTION_API_TOKEN") or "random_token"
    NOTION_DATABASE_URI = os.environ.get("DATABASE_URI")

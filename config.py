import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    NOTION_API_TOKEN = os.environ.get("NOTION_API_TOKEN") or "random_token"
    ARTIST_ADDRESS = os.environ.get("ARTIST_ADDRESS") or ""
    ARTIST_ZIP = os.environ.get("ARTIST_ZIP") or ""
    ARTIST_PHONE = os.environ.get("ARTIST_PHONE") or ""
    ARTIST_COUNTRY = os.environ.get("ARTIST_COUNTRY") or "Russia"
    ARTIST_CITY = os.environ.get("ARTIST_CITY") or ""
    ARTIST_LOGIN = os.environ.get("ARTIST_LOGIN") or ""
    ARTIST_PASS = os.environ.get("ARTIST_PASS") or ""

    ARTWORKS_ROOT_DIR = os.environ.get("ARTWORKS_DIR")
    NOTION_DATABASE_URI = os.environ.get("DATABASE_URI")

import os
from dotenv import load_dotenv, set_key

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    NOTION_API_TOKEN = os.environ.get("NOTION_API_TOKEN") or ""
    ARTIST_LOGIN = os.environ.get("ARTIST_LOGIN") or ""
    ARTIST_PASS = os.environ.get("ARTIST_PASS") or ""
    NOTION_LOGIN = os.environ.get("NOTION_LOGIN") or ""
    NOTION_PASS = os.environ.get("NOTION_PASS") or ""

    ARTWORKS_ROOT_DIR = os.environ.get("ARTWORKS_DIR") or ""
    NOTION_DATABASE_URI = os.environ.get("DATABASE_URI") or ""

    @classmethod
    def save_key(cls, key, value):
        fname = os.path.join(basedir, ".env")
        set_key(dotenv_path=fname, key_to_set=key, value_to_set=value)

    @classmethod
    def save_all(cls):
        members = [
            attr
            for attr in dir(cls)
            if not callable(getattr(cls, attr)) and not attr.startswith("__")
        ]
        for var in members:
            cls.save_key(cls, var, getattr(cls, var))
            print(var)

    @classmethod
    def set_key(cls, key, value):
        setattr(cls, key, value)


Config.set_key("NOTION_LOGIN", "1213")

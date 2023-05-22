import re
from notion_exporter.notion_exporter import NotionExporter


class NotionLogin:
    def __init__(self, email=None, password=None, token=None):
        if email:
            self.email = email
        if password:
            self.password = password
        if token:
            self.token = token
        self.notion = None

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        """
        Validate the email
        :param value:
        :return:
        """
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(pattern, value):
            self.__email = value
        else:
            raise ValueError(f"Invalid email address: {value}")

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        """
        Validate the token
        """
        pattern = r"v02%3Auser_token_or_cookies%3[A-Za-z0-9-_]{10,133}"
        if re.fullmatch(pattern, value):
            self.__token = value
        else:
            raise ValueError(f"Invalid token: {value}")

    def login(self):
        """
        Login to Notion
        :return:
        """
        # here we should connect
        try:
            self.notion = NotionExporter(self.token)
        except Exception as e:
            print(e)
            raise e
        return

    def getArtworks(self):
        notionArts = self.notion.export("de2f7e3c37324c10bd3a611389604f2e")
        return notionArts

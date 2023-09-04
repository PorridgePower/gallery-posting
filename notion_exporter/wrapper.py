import re
from notion_exporter.notion_exporter import NotionExporter


class NotionClient:
    def __init__(self):
        self.__email = self.__password = self.__token = None
        self._connection = None

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

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    def isActive(self):
        if self._connection is not None:
            return True

    def login(self):
        """
        Login to Notion
        :return:
        """
        # here we should connect
        try:
            if self.token:
                self._connection = NotionExporter(token_v2=self.token)
            elif self.email and self.password:
                self._connection = NotionExporter(
                    email=self.email, password=self.password
                )
        except Exception as e:
            raise Exception("Login failed!")
        return

    def getArtworks(self, db_id):
        notionArts = self._connection.export(db_id)
        return notionArts

    def getMultiselectValues(self, name):
        return self._connection.get_select_options(name)

    def updateArtworkState(self, art, value):
        self._connection.update_label(art, value)

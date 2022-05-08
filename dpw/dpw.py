import requests
from config import Config


class DPWSession:
    def __init__(self, username, password):
        self._user = username
        self._password = password
        self._session = requests.Session()
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
        }

    def login(self):
        login_data = {
            "LogonType": "NOT_JOINING",
            "UserName": self._user,
            "Password": self._password,
            "RememberMe": False,
            "RememberMe": False
        }
        resp = self._session.post(
            "https://www.dailypaintworks.com/Account/Logon", data=login_data
        )
        if resp.status_code != 200:
            print(resp.text)
            return False
        return True

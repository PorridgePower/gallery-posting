from re import T
from config import Config
from datetime import date, timedelta
from os import path, pread
import requests
import json


class Artwork:
    def __init__(self):
        self._keywords = []
        self._year = 2022
        self._art_height = 0
        self._art_width = 0
        self._art_depth = 0.1
        self._art_weight = 0.3
        self._art_title = ""
        self._art_description = ""
        self._art_price = 100

    @property
    def art_depth(self):
        return self._art_depth

    @property
    def art_weight(self):
        return self._art_weight

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, words):
        if not isinstance(words, list):
            raise TypeError("Keywords must be a list")
        if not len(words) in range(5, 12):
            raise ValueError("Use 5-12 keywords")
        self._keywords = words

    @property
    def art_price(self):
        return self._art_price

    @art_price.setter
    def art_price(self, value):
        if not isinstance(value, int):
            raise TypeError("Price must be a number")
        self._art_price = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if value > date.today().year:
            raise ValueError("Incorrect year")
        self._year = value

    @property
    def art_height(self):
        return self._art_height

    @art_height.setter
    def art_height(self, value):
        self._art_height = value

    @property
    def art_width(self):
        return self._art_width

    @art_width.setter
    def art_width(self, value):
        self._art_width = value

    @property
    def art_title(self):
        return self._art_title

    @art_title.setter
    def art_title(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if not len(title) in range(3, 10):
            raise ValueError("Use 3-10 characters")
        self._art_title = title

    @property
    def art_description(self):
        return self._art_description

    @art_description.setter
    def art_description(self, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        if len(description) < 50:
            raise ValueError(
                "Minimum characters for description still required 50")
        self._art_description = description

    @property
    def art_mediums(self):
        return self._art_mediums

    @art_mediums.setter
    def art_mediums(self, words):
        if not isinstance(words, list):
            raise TypeError("Meduims must be a list")
        if not len(words) > 0:
            raise ValueError("Set at least 1 medium")
        self._art_mediums = words

    @property
    def art_materials(self):
        return self._art_materials

    @art_materials.setter
    def art_materials(self, words):
        if not isinstance(words, list):
            raise TypeError("Materials must be a list")
        if not len(words) > 0:
            raise ValueError("Set at least 1 material")
        self._art_materials = words

    @property
    def art_styles(self):
        return self._art_styles

    @art_styles.setter
    def art_styles(self, words):
        if not isinstance(words, list):
            raise TypeError("Styles must be a list")
        if not len(words) > 0:
            raise ValueError("Set at least 1 style")
        self._art_styles = words

    def initialize(self, title, height, width, keywords, description, year, price, mediums, materials, styles, subject):
        self.keywords = keywords
        self.year = year
        self.art_height = height
        self.art_width = width
        self.art_title = title
        self.art_description = description
        self.art_price = price * 0.7
        self.art_mediums = mediums
        self.art_materials = materials
        self.art_styles = styles
        self.art_subject = subject


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
            "RememberMe": "true",
            "RememberMe": "true"
        }
        # resp = self._session.post(
        #     "https://www.dailypaintworks.com/Account/Logon", data=login_data
        # )
        req = requests.Request(
            "POST", "https://www.dailypaintworks.com/Account/Logon", data=login_data)
        prepped = req.prepare()
        resp = self._session.send(prepped)
        if resp.status_code != 200:
            print(resp.text)
            return False
        return True

    def upload_art(self, art, image):
        resp = self._session.get(
            "https://www.dailypaintworks.com/account/arttracking")

        self._session.cookies.set(
            "dpw-lastArtistDestination", "/Account/artTracking", domain="www.dailypaintworks.com")
        resp = self._session.get(
            "https://www.dailypaintworks.com/ui/ArtworkWizard")

        resp = self._session.post(
            "https://www.dailypaintworks.com/ui/GetArtworkWizardData/", data='inPostId=null&inClone=false')

        next_day = date.today() + timedelta(days=1)
        upload_request = {
            "useSmartFormResult": "false",
            "PostId": "",
            "RemoveSecondImage": "false",
            "Hide": "false",
            "CreatedDate": "{}/{}".format(date.today().strftime("%m/%d"), str(art.year)),
            "Title": art.art_title,
            "Show": "showEverywhere",
            "FrontPageDate": next_day.strftime("%m/%d/%Y"),
            "PostStatusCode": "AVAILABLE",
            "StatusChangeDate": "",
            "CurrencyCode": "USD",
            "Price": '{0:.2f}'.format(art.art_price),
            "SalesTax": "0.00",
            "Shipping": "0.00",
            "PaidDate": "",
            "ShippedDate": "",
            "Keywords": ','.join(str(k) for k in art.keywords),
            "CategoryId": 2,  # unknown
            "MediaId": 3,  # unknown
            "MediaDetails": "",
            "PaintingHeight": art.art_height,
            "PaintingWidth": art.art_width,
            "UnitCode": "CM",
            "Description": "<p>{}</p>".format(art.art_description),
            "VideoUrl": "",
            "Notes": "",
            "SellUrl": ""}

        files = {}
        for k in upload_request.keys():
            files[k] = (None, upload_request[k], None)
        files['MainImageFile'] = (path.basename(
            image), open(image, 'rb'), 'image/jpeg')
        resp = self._session.post(
            "https://www.dailypaintworks.com/ui/ArtworkWizardUpdate/",
            files=files,
        )

        if resp.status_code != 200:
            print(resp.text)
            return False
        return True

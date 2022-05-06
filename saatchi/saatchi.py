from pickletools import uint8
import requests
import json
from config import Config
from os import path
from datetime import date
import time

category = 164  # always set "Painting" for me
subject = 204  # 242 - absract, 204 - landscape
mediums = ["Watercolor"]
materials = ["Paper"]
styles = ["Abstract"]

artist_address_street = Config.ARTIST_ADDRESS
artist_address_unit = ""
artist_address_city = Config.ARTIST_CITY
artist_address_country = Config.ARTIST_COUNTRY
artist_address_country_iso2 = "RU"
artist_address_region = Config.ARTIST_CITY
artist_address_zip = Config.ARTIST_ZIP
artist_phone = Config.ARTIST_PHONE


class SaatchiArtwork:
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
    def price(self):
        return self.price

    @price.setter
    def price(self, value):
        if not isinstance(value, int):
            raise TypeError("Price must be a number")
        if value < 100:
            raise ValueError("For Saatchi price must be over 100$")
        self._price = value

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
        if not len(title) in range(3, 100):
            raise ValueError("Use 3-100 characters")
        self._art_title = title

    @property
    def art_description(self):
        return self._art_description

    @art_description.setter
    def art_description(self, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        if len(description) < 50:
            raise ValueError("Minimum characters for description still required 50")
        self._art_description = description

    def initialize(self, title, height, width, keywords, description, year, price):
        self.keywords = keywords
        self.year = year
        self.art_height = height
        self.art_width = width
        self.art_title = title
        self.art_description = description
        self.art_price = price


class SaatchiSession:
    def __init__(self, username, password):
        self._user = username
        self._password = password
        self._session = requests.Session()
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
        }

    def login(self):
        login_data = {
            "remember": "false",
            "captchaAction": "login_submit",
            "email": self._user,
            "password": self._password,
        }
        resp = self._session.post(
            "https://www.saatchiart.com/auth-api/login", data=login_data
        )
        if resp.status_code != 200:
            print(resp.text)
            return False
        return True

    def _upload_img(self, local_path):
        files = {"Filedata": open(local_path, "rb")}
        resp = self._session.post("https://upload.saatchiart.com/", files=files)
        if resp.status_code != 200:
            print(resp.text)
            return {}
        resp_json = json.loads(resp.text)
        return resp_json

    def upload_photo(self, local_path):
        if not path.exists(local_path):
            print("File {lacal_path} does not exist!")
            return False
        upload_result = self._upload_img(local_path)
        return upload_result

    def upload_art(self, art, image):
        self.uploaded_image_info = self.upload_photo(image)
        upload_request = {
            "weight_unit": "CENTIMETER",
            "size_unit": "CENTIMETER",
            "thumbnail": self.uploaded_image_info["server"]
            + "?img="
            + self.uploaded_image_info["thumbURL"],
            "original_file": self.uploaded_image_info["originalFile"],
            "sold_status": "avail",
            "is_available_for_prints": False,
            "is_copyright_owner": True,
            "is_multipaneled": False,
            "is_framed": False,
            "is_banned": False,
            "date_created": art.year,
            "category": category,
            "subject": subject,
            "mediums": mediums,
            "materials": materials,
            "styles": styles,
            "keywords": art.keywords,
            "art_height": art.art_height,
            "art_width": art.art_width,
            "art_depth": art.art_depth,
            "art_title": art.art_title,
            "art_description": art.art_description,
            "art_weight": art.art_weight,
            "art_price": art.art_price,
            "container_weight": 0,
            "artist_address_street": artist_address_street,
            "artist_address_unit": artist_address_unit,
            "artist_address_city": artist_address_city,
            "artist_address_country": artist_address_country,
            "artist_address_region": artist_address_region,
            "artist_address_zip": artist_address_zip,
            "artist_phone": artist_phone,
            "shipping_type": "rolled",
            "canvas_wrap_color": 38,
            "file_width": self.uploaded_image_info["originalWidth"],
            "file_height": self.uploaded_image_info["originalHeight"],
            "print_pricing_slider": 0,
            "is_limited_light_artist": False,
            "is_admin": False,
            "productType": None,
            "selectedOfferingDataMap": {},
            "listed_not_for_sale": False,
            "listed_no_prints": False,
            "preferredLocale": "en-US",
            "artist_address_country_iso2": artist_address_country_iso2,
        }

        time.sleep(10)
        resp = self._session.post(
            "https://www.saatchiart.com/upload/beta-submit",
            data=json.dumps(upload_request),
        )

        if resp.status_code != 200:
            return False
        print(
            "Uploaded art URL: https://www.saatchiart.com/%s"
            % json.loads(resp.text)["redirect_url"]
        )
        return True

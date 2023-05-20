from pickletools import uint8
import requests
import json
from config import Config
from os import path
from datetime import date
import time
from PIL import Image


category = "Painting"  # always set "Painting" for me
subject = "Landscape"  # 242 - absract, 204 - landscape
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


def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    return (width, height)


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
    def art_price(self):
        return self._art_price

    @art_price.setter
    def art_price(self, value):
        if not isinstance(value, int):
            raise TypeError("Price must be a number")
        if value < 100:
            raise ValueError("For Saatchi price must be over 100$")
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

    def initialize(
        self,
        title,
        height,
        width,
        keywords,
        description,
        year,
        price,
        mediums,
        materials,
        styles,
        subject,
    ):
        self.keywords = keywords
        self.year = year
        self.art_height = height
        self.art_width = width
        self.art_title = title
        self.art_description = description
        self.art_price = price
        self.art_mediums = mediums
        self.art_materials = materials
        self.art_styles = styles
        self.art_subject = subject


class SaatchiSession:
    UPLOAD_URL = "https://www.saatchiart.com"

    def __init__(self, username, password):
        self._user = username
        self._password = password
        self._session = requests.Session()
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
        }

    def get_error_msg(self, response):
        errors = response.get("message")
        if not errors:
            errors = ". ".join(response.get("errorMessages"))

        return errors if errors else "Unkown error!"

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
            raise Exception(f"Login failed")
        return True

    def _upload_img(self, local_path):
        files = {"image": open(local_path, "rb")}
        resp = self._session.post(
            f"{self.UPLOAD_URL}/easel_api/my-art/image/upload", files=files
        )
        resp_json = json.loads(resp.text)
        if resp.status_code != 200:
            errors = self.get_error_msg(resp_json)
            raise Exception(errors)
        else:
            return resp_json["payload"]["url"]

    def upload_photo(self, local_path, title):
        if not path.exists(local_path):
            raise Exception("File {local_path} does not exist!")
        image_url = self._upload_img(local_path)
        min_dimension = min(get_num_pixels(local_path))
        save_image_request = {
            "crops": {
                "square": {
                    "x": 0,
                    "y": 0,
                    "width": min_dimension,
                    "height": min_dimension,
                },
                "scale": {
                    "x": 0,
                    "y": 0,
                    "width": min_dimension,
                    "height": min_dimension,
                },
            },
            "s3StagingPath": image_url,
            "title": title,
            "step": "image",
        }
        resp = self._session.post(
            f"{self.UPLOAD_URL}/easel_api/my-art/upload",
            json=save_image_request,
        )
        resp_json = json.loads(resp.text)
        if resp.status_code != 200:
            errors = self.get_error_msg(resp_json)
            raise Exception(errors)
        return resp_json["payload"]["artwork_id"]

    def publish_art(self, ardwok_id):
        resp = self._session.put(
            f"{self.UPLOAD_URL}/easel_api/my-art/{ardwok_id}/publish"
        )
        resp_json = json.loads(resp.text)
        if resp.status_code != 200:
            errors = self.get_error_msg(resp_json)
            raise Exception(errors)

    def update_description(self, art, ardwok_id):
        description = {
            "artworkId": ardwok_id,
            "category": category,
            "description": art.art_description,
            "dimensions": {
                "width": art.art_width,
                "height": art.art_height,
                "depth": art.art_depth,
            },
            "keywords": art.keywords,
            "materials": art.art_materials,
            "mediums": art.art_mediums,
            "styles": art.art_styles,
            "subject": subject,
            "yearProduced": art.year,
            "step": "description",
        }
        resp = self._session.put(
            f"{self.UPLOAD_URL}/easel_api/my-art/{ardwok_id}/update",
            json=description,
        )
        resp_json = json.loads(resp.text)
        if resp.status_code != 200:
            errors = self.get_error_msg(resp_json)
            raise Exception(errors)

    def upload_art(self, art, image):
        try:
            ardwok_id = self.upload_photo(image, art.art_title)
            self.update_description(art, ardwok_id)
            self.publish_art(ardwok_id)
        except Exception as e:
            print(e)
            return False
        return True

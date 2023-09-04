import requests
import json
from os import path
import time
from PIL import Image
from config import Config
from ..artwork import Artwork


category = "Painting"  # always set "Painting" for me
subject = "Landscape"  # 242 - absract, 204 - landscape
mediums = ["Watercolor"]
materials = ["Paper"]
styles = ["Abstract"]


def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    return (width, height)


class SaatchiSession:
    UPLOAD_URL = "https://www.saatchiart.com"

    def __init__(self, username, password):
        self._user = username
        self._password = password
        self._session = requests.Session()
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
        }

    def prepare_art(art):
        prepared_art = Artwork()

        keywords = Artwork.str2list(art.get_property("keywords"))
        year = art.get_property("year") or "2022"
        art_height = art.get_property("height") or "10"
        art_width = art.get_property("width") or "10"
        art_title = art.get_property("name") or "Unnamed"
        art_description = art.get_property("description")
        art_price = art.get_property("price") or "100"
        art_dir = art.get_property("folder")

        art_mediums = Artwork.str2list(art.get_property("mediums"))
        art_materials = Artwork.str2list(art.get_property("materials"))
        art_styles = Artwork.str2list(art.get_property("styles"))
        art_subject = art.get_property("subject")

        prepared_art.initialize(
            art_title,
            int(art_height),
            int(art_width),
            keywords,
            art_description,
            int(year),
            int(art_price),
            art_mediums,
            art_materials,
            art_styles,
            art_subject,
        )

        return prepared_art

    def get_error_msg(self, response):
        print(response)
        err = None
        err = response.get("message")
        if not err:
            errors = response.get("errorMessages")
            if errors:
                err = ". ".join(errors)
        return err if err else "Unkown error!"

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
            raise Exception(f"Login to Saatchi failed")

        resp_json = json.loads(resp.text)
        if resp_json.get("messages"):
            raise Exception(f"Login to Saatchi failed")

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
        time.sleep(5)
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
            raise e

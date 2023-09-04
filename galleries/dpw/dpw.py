from config import Config
from datetime import date, timedelta
from os import path, pread
import requests
from ..artwork import Artwork


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
            "RememberMe": "true",
        }
        # resp = self._session.post(
        #     "https://www.dailypaintworks.com/Account/Logon", data=login_data
        # )
        req = requests.Request(
            "POST", "https://www.dailypaintworks.com/Account/Logon", data=login_data
        )
        prepped = req.prepare()
        resp = self._session.send(prepped)
        if resp.status_code != 200:
            print(resp.text)
            raise ("Login to DaylyPaintWorks failed!")
        return True

    def upload_art(self, art, image):
        resp = self._session.get("https://www.dailypaintworks.com/account/arttracking")

        self._session.cookies.set(
            "dpw-lastArtistDestination",
            "/Account/artTracking",
            domain="www.dailypaintworks.com",
        )
        resp = self._session.get("https://www.dailypaintworks.com/ui/ArtworkWizard")

        resp = self._session.post(
            "https://www.dailypaintworks.com/ui/GetArtworkWizardData/",
            data="inPostId=null&inClone=false",
        )
        # print(resp.text)

        next_day = date.today() + timedelta(days=1)
        upload_request = {
            "useSmartFormResult": "false",
            "PostId": "",
            "RemoveSecondImage": "false",
            "Hide": "false",
            "CreatedDate": "{}/{}".format(
                date.today().strftime("%m/%d"), str(art.year)
            ),
            "Title": art.art_title,
            "Show": "showEverywhere",
            "FrontPageDate": next_day.strftime("%m/%d/%Y"),
            "PostStatusCode": "AVAILABLE",
            "StatusChangeDate": "",
            "CurrencyCode": "USD",
            "Price": "{0:.2f}".format(art.art_price),
            "SalesTax": "0.00",
            "Shipping": "0.00",
            "PaidDate": "",
            "ShippedDate": "",
            "Keywords": ",".join(str(k) for k in art.keywords),
            "CategoryId": 2,  # unknown
            "MediaId": 3,  # unknown
            "MediaDetails": "",
            "PaintingHeight": art.art_height,
            "PaintingWidth": art.art_width,
            "UnitCode": "CM",
            "Description": "<p>{}</p>".format(art.art_description),
            "VideoUrl": "",
            "Notes": "",
            "SellUrl": "",
        }

        files = {}
        for k in upload_request.keys():
            files[k] = (None, upload_request[k], None)
        files["MainImageFile"] = (path.basename(image), open(image, "rb"), "image/jpeg")
        resp = self._session.post(
            "https://www.dailypaintworks.com/ui/ArtworkWizardUpdate/",
            files=files,
        )
        raise Exception("Unauthorized access")

        if resp.status_code != 200:
            print(resp.text)
            raise Exception(resp.text)
        return True

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

from os import path, listdir
from datetime import date


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

    def find_main_image(directory):
        if not path.exists(directory):
            return ""
        images = [
            f
            for f in sorted(listdir(directory))
            if path.join(directory, f.lower()).endswith(".jpg")
        ]
        for i in images:
            if i.startswith("re_"):
                return path.join(directory, i)
        return ""

    def str2list(line):
        return [x.strip() for x in line.split(",")]

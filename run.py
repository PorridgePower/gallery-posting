from email.mime import image
from genericpath import exists
from re import IGNORECASE
from saatchi.saatchi import SaatchiSession, SaatchiArtwork
from config import Config
from os import path, listdir
from notion_exporter.notion_exporter import NotionExporter


def main():
    email = Config.ARTIST_LOGIN
    password = Config.ARTIST_PASS
    notion = NotionExporter(Config.NOTION_API_TOKEN)
    notionArts = notion.export(Config.NOTION_DATABASE_URI)

    for notionArtData in notionArts:
        art = SaatchiArtwork()

        keywords = str2list(notionArtData.get_property("keywords"))
        year = notionArtData.get_property("year") or "2022"
        art_height = notionArtData.get_property("height") or "10"
        art_width = notionArtData.get_property("width") or "10"
        art_title = notionArtData.get_property("name") or "Unnamed"
        art_description = notionArtData.get_property("description")
        art_price = notionArtData.get_property("price") or "100"
        art_dir = notionArtData.get_property("folder")

        art_mediums = str2list(notionArtData.get_property("mediums"))
        art_materials = str2list(notionArtData.get_property("materials"))
        art_styles = str2list(notionArtData.get_property("styles"))
        art_subject = notionArtData.get_property("subject")

        image_path = find_main_image(path.join(Config.ARTWORKS_ROOT_DIR,
                                               art_dir))
        if image_path == "":
            print("No photo for arwork was found")
            exit(1)
        art.initialize(art_title, int(art_height), int(art_width),
                       keywords, art_description, int(year), int(art_price), art_mediums, art_materials, art_styles, art_subject)

        saatchiSession = SaatchiSession(email, password)
        saatchiSession.login()
        saatchiSession.upload_art(art, image_path)


def find_main_image(directory):
    if not path.exists(directory):
        return ""
    images = [f for f in sorted(listdir(directory)) if path.join(
        directory, f.lower()).endswith(".jpg")]
    print(images)
    for i in images:
        if i.startswith("re_"):
            return path.join(directory, i)
    return ""


def str2list(line):
    return [x.strip()
            for x in line.split(',')]


if __name__ == "__main__":
    main()

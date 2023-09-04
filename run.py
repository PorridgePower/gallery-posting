from email.mime import image
from genericpath import exists
from re import IGNORECASE
from galleries.saatchi.saatchi import SaatchiSession
from galleries.artwork import Artwork
from config import Config
from os import path, listdir
from notion_exporter.notion_exporter import NotionExporter


def main():
    email = Config.ARTIST_LOGIN
    password = Config.ARTIST_PASS
    notion = NotionExporter(Config.NOTION_API_TOKEN)
    notionArts = notion.export(Config.NOTION_DATABASE_URI)

    saatchiSession = SaatchiSession(email, password)
    saatchiSession.login()
    for notionArtData in notionArts:
        notion.update_label(notionArtData, "dpw")
        prep_art = Artwork()
        prep_art = SaatchiSession.prepare_art(notionArtData)
        image_path = Artwork.find_main_image(
            path.join(Config.ARTWORKS_ROOT_DIR, notionArtData.get_property("folder"))
        )
        if image_path == "":
            print("No photo for arwork was found")
            exit(1)

        saatchiSession.upload_art(prep_art, image_path)


def find_main_image(directory):
    if not path.exists(directory):
        return ""
    images = [
        f
        for f in sorted(listdir(directory))
        if path.join(directory, f.lower()).endswith(".jpg")
    ]
    print(images)
    for i in images:
        if i.startswith("re_"):
            return path.join(directory, i)
    return ""


def str2list(line):
    return [x.strip() for x in line.split(",")]


if __name__ == "__main__":
    main()

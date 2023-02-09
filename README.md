# gallery-posting
Tool for publishing artworks to online galleries

## Requirements

 `pip install -r requirements.txt`

## How does it works

This tool was designed to automate the upload my artworks with common info to [SaatchiArt](https://www.saatchiart.com/), [DailyPaintworks](https://www.dailypaintworks.com/) and [Artfinder](https://www.artfinder.com/#/)
using Notion database.

The database (table) has the following structure:

<img src="https://user-images.githubusercontent.com/62947325/217303497-a3da9eab-c521-4580-9f4a-7597f7235516.png" width="600" height="350">

Each page includes common artwork's properties

<img src="https://user-images.githubusercontent.com/62947325/217301913-b7c0dab7-2688-4c9e-b92f-dd571c061fe1.png" width="800" height="750">

Only not posted artworks will be selected for upload. After successfull upload "Posted" column value will be changed to "Yes".

## Usage

1. Define enviroment variables:

```
NOTION_API_TOKEN=<Notion api token>
ARTWORKS_DIR = <root directory with atrworks>
ARTIST_LOGIN = <login>
ARTIST_PASS = <password>
ARTIST_ADDRESS = <address>
ARTIST_CITY= <cisy>
ARTIST_ZIP = <post code>
ARTIST_PHONE = <nomber>
ARTIST_COUNTRY = <country>
```

2. Then run
`python3 run.py`

## TODO
* Unit tests
* Update for current notion API
* Dynamic selection of category, subject, mediums, styles and materials, not hardcoded
* Add friendly UI

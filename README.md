# single_file_scrapers

These are some Python 3 web scraping scripts that I've written for my own personal use. They follow this set of criteria which I have an eye for:

 - Does not use official APIs.
 - Minimal library usage (BeautifulSoup4 and not much else).
 - Uses `wget`, `youtube-dl`, `ffmpeg`, and equally widespread inobscure tools.
 - Simple repeatable behavior (URL goes in, new folder with files comes out).
 - Repeatability! If the same command is run in the same place, it will not redownload/overwrite files.

I will be accepting contributions.

Inspired by nothings's [*single_file_libs*](https://github.com/nothings/single_file_libs).

## scripts


### reddit.com

| script                                          | requires                | license      | description
| ----------------------------------------------- |:-----------------------:|:------------:| -----------
| [scrape_reddit.py](scrape_reddit.py)            | wget, youtube-dl        | CC BY-SA 4.0 | Downloads images and video from reddit listing pages. See file for specific domains/media types.

### 4chan.org

| script                                          | requires                | license      | description
| ----------------------------------------------- |:-----------------------:|:------------:| -----------
| [scrape_4chan.py](scrape_4chan.py)              | BeautifulSoup4, wget    | CC BY-SA 4.0 | Downloads media from 4chan threads.
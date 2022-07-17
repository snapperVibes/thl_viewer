from os import path
from typing import Literal

import bs4
import httpx
import logging

logger = logging.getLogger(__name__)
logger.level = logging.INFO
logger.addHandler(logging.StreamHandler())

def make_url(
    conference, season, week: int | Literal["current-week", "previous-week"]
) -> str:
    if type(week) == int:
        _week = f"week-{str(week)}"
    else:
        _week = str(week)
    return f"https://www.teamhearthleague.com/{conference}-s{season}---{_week}.html"


def scrape(conf, season, week):
    url = make_url(conf, season, week)
    resp = httpx.get(url)
    if resp.status_code == 404:
        resp.raise_for_status()

    soup = bs4.BeautifulSoup(resp.content, features="html.parser")
    iframe = soup.find("iframe")
    link = iframe["src"]

    resp = httpx.get(link)
    file_name = f"{season}-{conf}-{week}.html"
    file_path = path.join("scraped", file_name)
    with open(file_path, "wb") as f:
        f.write(resp.content)
        logger.info("Wrote %s" % file_path)


seasons = [6]
confs = ["green", "brown"]
numeric_weeks = range(1, 14)
special_weeks = ["previous-week", "current-week"]

if __name__ == '__main__':
    for season in seasons:
        for conf in confs:
            for week in numeric_weeks:
                try:
                    scrape(conf, season, week)
                # Todo: make this explicitly catch only 404s
                except httpx.HTTPStatusError:
                    break
            for week in special_weeks:
                scrape(conf, season, week)

import datetime
import os
import re
import time
from collections import namedtuple
from functools import partial
from itertools import islice, dropwhile, takewhile
from typing import Generator, Any

import pandas as pd
from bs4 import BeautifulSoup, Tag, PageElement

import database
from database import engine
from sqlmodel import Session, SQLModel, select

import models
from operations import select_or_insert

SCRAPED = "scraped"
#
# https://docs.google.com/spreadsheets/d/e/2PACX-1vQeGoLTnkKL439bxAAACBqvAW9gL2qjgvX6aqaqhfAdL1EDi5YATnMtqs63Ef-kankktLgoupi-giy4/pubhtml?gid=899051774&single=true&single=true&widget=false&headers=false&chrome=false
def parse_soup(db, soup: BeautifulSoup):
    # Examples on right
    _table_elem = soup.find("tbody")
    _rows = _table_elem.find_all("tr")
    rows = (row.find_all("td") for row in _rows)


    # Consume header rows
    rows.__next__()
    r2 = rows.__next__()
    page_info = r2[1].text  # "Wild Series - Season 6, Week 1"
    pattern = re.compile(r"(?P<series>.*)\sSeries\s-\sSeason\s(?P<season>.*),\sWeek\s(?P<week>.*)")
    match_obj = re.match(pattern, page_info)
    if pattern is None:
        raise RuntimeError()
    d = match_obj.groupdict()
    _series = d["series"]
    _season = d["season"]
    _week = d["week"]

    season = models.Season(name=str(_season))
    select_or_insert.season(db, season)
    db.refresh(season)
    series = models.Series(name=_series, season_id=season.id)

    select_or_insert.series(db, series)

    _date = r2[15].text  # "5/23/2022"
    date = time.strptime(_date, "%m/%d/%Y")


    r3 = rows.__next__()
    _conference = r3[1].text  # "Brown Conference"
    conference = _conference.removesuffix(" Conference")
    matches = [consume_match(rows) for _ in range(7)]





def consume_match(rows: Generator[list[PageElement], Any, None]):
    r = rows.__next__()
    home_team = r[1]
    away_team = r[4]

    r = rows.__next__()
    home_team_total_pts = r[6]
    home_team_total_record = r[7]
    away_team_total_record = r[10]
    away_team_total_pts = r[11]

    r = rows.__next__()
    home_team_ts = r[8]
    away_team_pts = r[11]

    rows.__next__()
    rows.__next__()

    sets = [consume_set(rows) for _ in range(5)]
    r = rows.__next__()
    team1_capt = r[2].text
    team2_capt = r[13].text


def consume_set(rows):
    r = rows.__next__()

    p1_total_pts = r[1].text
    p1_name = r[2].text
    _p1_decks_link = r[3].find("a")
    p1_d0nky = None if _p1_decks_link is None else _p1_decks_link["href"]
    p1_deck1 = r[3].text
    p1_deck2 = r[4].text
    p1_deck3 = r[5].text
    p1_deck4 = r[6].text
    p1_ban = r[8].text

    set_pts = r[9].text

    p2_total_pts = r[12].text
    p2_name = r[13].text
    _p2_decks_link = r[14].find("a")
    p2_d0nky = None if _p2_decks_link is None else _p2_decks_link["href"]
    p2_deck1 = r[14].text
    p2_deck2 = r[15].text
    p2_deck3 = r[16].text
    p2_deck4 = r[17].text
    p2_ban = r[19].text









with Session(database.engine) as db:
    for filename in os.listdir(SCRAPED):
        with open(os.path.join(SCRAPED, filename)) as f:
            soup = BeautifulSoup(f.read(), features="lxml")
            parse_soup(db, soup)
    db.commit()




from datetime import datetime as DateTime
import os
import re
import time

from typing import Generator, Any

from bs4 import BeautifulSoup, PageElement

import database
from database import engine
from sqlmodel import Session, SQLModel, select

import models
from operations import select_or_insert

SCRAPED = "scraped"
#
# https://docs.google.com/spreadsheets/d/e/2PACX-1vQeGoLTnkKL439bxAAACBqvAW9gL2qjgvX6aqaqhfAdL1EDi5YATnMtqs63Ef-kankktLgoupi-giy4/pubhtml?gid=899051774&single=true&single=true&widget=false&headers=false&chrome=false
def parse_soup(soup: BeautifulSoup):
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

    _date = r2[15].text  # "5/23/2022"
    _date = time.strptime(_date, "%m/%d/%Y")
    _date = DateTime.fromtimestamp(time.mktime(_date))

    r3 = rows.__next__()
    _conference = r3[1].text  # "Brown Conference"
    _conference = _conference.removesuffix(" Conference")
    _sets = [consume_set(rows) for _ in range(7)]




    series = select_or_insert.series(db, name=_series)
    season = select_or_insert.season(db, number=int(_season), series=series)
    week = select_or_insert.week(db, number=int(_week), season=season)
    conference = select_or_insert.conference(db, name=_conference, season=season)
    ## Todo: make it elegant later
    # sets = [select_or_insert.set(db, week=week, conference=conference) for _ in _sets]
    # for set_ in sets:
    #     matches = [select_or_insert.match(db, set=set) for match in _sets["match"]]



    for _set in _sets:
        set_ = select_or_insert.set(db, week=week, conference=conference)
        for match in _set["matches"]:
            match = select_or_insert.m





    # Now, create each model
    _series, _season, _week, _sets


def parse_record(record):
    """ Returns a triple of wins, losses, and ties"""
    match str(record).split("-"):
        case wins, losses:
            ties = 0
        case wins, losses, ties:
            pass
        case _:
            breakpoint()
            raise RuntimeError("Unparsable record")
    return wins, losses, ties

def consume_set(rows: Generator[list[PageElement], Any, None]) -> dict:
    r = rows.__next__()
    _home_team = r[1].text
    _away_team = r[4].text

    r = rows.__next__()
    _home_team_total_pts = r[6].text  # 134 pts
    _home_team_total_record = r[7].text  # 6-1-1
    _away_team_total_record = r[10].text
    _away_team_total_pts = r[11].text

    r = rows.__next__()
    _home_team_pts = r[8].text
    _away_team_pts = r[11].text

    rows.__next__()
    rows.__next__()

    match_details = [consume_match(rows) for _ in range(5)]

    r = rows.__next__()
    _team1_capt = r[2].text
    _team2_capt = r[13].text



    standings = []
    for team, _record, _points in zip(
            (_home_team, _away_team),
            (_home_team_total_record, _away_team_total_record),
            (_home_team_total_pts, _away_team_pts),
    ):
        record = _record
        points = int(str(_points).removesuffix(" pts"))
        wins, losses, ties = parse_record(record)
        # Todo


def consume_match(rows):
    r = rows.__next__()

    p1_total_pts = r[1].text
    p1_name = r[2].text
    _p1_decks_link = r[3].find("a")
    p1_deck_link = None if _p1_decks_link is None else _p1_decks_link["href"]
    p1_deck1 = r[3].text
    p1_deck2 = r[4].text
    p1_deck3 = r[5].text
    p1_deck4 = r[6].text
    p1_ban = r[8].text

    set_pts = r[9].text

    p2_total_pts = r[12].text
    p2_name = r[13].text
    _p2_decks_link = r[14].find("a")
    p2_deck_link = None if _p2_decks_link is None else _p2_decks_link["href"]
    p2_deck1 = r[14].text
    p2_deck2 = r[15].text
    p2_deck3 = r[16].text
    p2_deck4 = r[17].text
    p2_ban = r[19].text

    # return models.Match(
    #     week_id=we
    # )








if __name__ == '__main__':
    with Session(database.engine) as db:
        for filename in os.listdir(SCRAPED):
            with open(os.path.join(SCRAPED, filename)) as f:
                soup = BeautifulSoup(f.read(), features="lxml")
                parse_soup(soup)
        db.commit()




from sqlmodel import Session, select

from models import *

# fmt: off

def series(db, name):
    statement = select(Series).where(Series.name == name)
    return db.exec(statement).one_or_none()

def season(db, *, number, series):
    statement = select(Season).where(Season.number == number, Season.series == series)
    return db.exec(statement).one_or_none()

def week(db, *, number, season):
    statement = select(Week).where(Week.number == number, Week.season == season)
    return db.exec(statement).one_or_none()


def conference(db, *, name, season) -> Conference:
    statement = select(Conference).where(Conference.name == name, Conference.season == season)
    return db.exec(statement).one_or_none()


def set(db, *, week, conference) -> Set:
    model = Set(week=week, conference=conference)
    db.add(model)
    return model

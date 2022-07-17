from models import *

def series(db, *, name: str) -> Series:
    model = Series(name=name)
    db.add(model)
    return model

def season(db, *, number, series) -> Season:
    model = Season(number=number, series=series)
    db.add(model)
    return model

def week(db, *, number, season) -> Week:
    model = Week(number=number, season=season)
    db.add(model)
    return model


def conference(db, *, name, season) -> Conference:
    model = Conference(name=name, season=season)
    db.add(model)
    return model


def set(db, *, week, conference) -> Set:
    model = Set(week=week, conference=conference)
    db.add(model)
    return model
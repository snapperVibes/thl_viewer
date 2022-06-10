from sqlmodel import Session, select

from models import *



def season(db: Session, model):
    statement = select(Season).where(Season.name == model.name)
    return db.exec(statement).one_or_none()


def series(db: Session, model):
    statement = select(Series).where(Series.name == model.name, Series.season_id == model.season_id)
    return db.exec(statement).one_or_none()
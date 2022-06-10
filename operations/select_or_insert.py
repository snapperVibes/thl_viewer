from models import *
from operations import select

def _select_or_insert(db, select_, model):
    output = select_(db, model)
    if output is None:
        output = db.add(model)
    return output


def season(db, model: Season) -> Season:
    return _select_or_insert(db, select.season, model)


def series(db, model):
    return _select_or_insert(db, select.series, model)
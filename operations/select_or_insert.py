from operations import select, insert


def _select_or_insert(db, select_, insert_, **kwargs):
    output = select_(db, **kwargs)
    if output is None:
        output = insert_(db, **kwargs)
    return output


def series(db, *, name):
    return _select_or_insert(db, select.series, insert.series, name=name)
def season(db, *, number, series):
    return _select_or_insert(db, select.season, insert.season, number=number, series=series)
def week(db, *, number, season):
    return _select_or_insert(db, select.week, insert.week, number=number, season=season)
def set(db, *, week, conference):
    return _select_or_insert(db, select.set, insert.set, week=week, conference=conference)


def conference(db, *, name, season):
    return _select_or_insert(db, select.conference, insert.conference, name=name, season=season )
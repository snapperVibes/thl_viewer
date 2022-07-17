import operations.select_or_insert
from main import create_db_and_tables
from sqlmodel import Session
import models
import database

create_db_and_tables()

with Session(database.engine) as db:
    series = "Wild"
    model = models.Series(name=series)
    operations.select_or_insert.series(db, model)
    db.commit()
    pass




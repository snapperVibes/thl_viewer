from sqlmodel import create_engine

from models import *

sqlite_file_name = "thl.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_db_and_tables()

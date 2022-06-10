from sqlmodel import create_engine

from models import *

sqlite_file_name = "thl.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True).execution_options()

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine.execution_options)

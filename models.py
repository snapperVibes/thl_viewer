# TODO: Unique indexes

from typing import Optional, List, Any
from datetime import datetime as DateTime
from sqlalchemy import func

from sqlmodel import SQLModel, Field, Relationship


class _BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)


# Todo: I don't fully understand what each section is, and thus have not named them
#  I do believe they are seperate though

####################################################################
### Section 1 ###

class Series(_BaseModel, table=True):
    __tablename__ = "series"
    name: str

    seasons: list["Season"] = Relationship(back_populates="series")


class Season(_BaseModel, table=True):
    __tablename__ = "seasons"
    number: int
    series_id: Optional[int] = Field(default=None, foreign_key="series.id")

    series: Optional[Series] = Relationship(back_populates="seasons")
    weeks: list["Week"] = Relationship(back_populates="season")
    conferences: list["Conference"] = Relationship(back_populates="season")


class Week(_BaseModel, table=True):
    __tablename__ = "weeks"
    number: int
    season_id: Optional[int] = Field(default=None, foreign_key="seasons.id")
    # Todo? Whether a week is a playoff week isn't stored. Perhaps it should be stored

    season: Optional[Season] = Relationship(back_populates="weeks")


class Conference(_BaseModel, table=True):
    __tablename__ = "conferences"
    name: str
    season_id: Optional[int] = Field(default=None, foreign_key="seasons.id")

    season: Optional[Season] = Relationship(back_populates="conferences")


class Set(_BaseModel, table=True):
    __tablename__ = "sets"
    week_id: Optional[int] = Field(default=None, foreign_key="weeks.id")
    conference_id: Optional[int] = Field(default=None, foreign_key="conferences.id")

    week: Optional[Week] = Relationship()
    conference: Optional[Conference] = Relationship()
    matches: list["Match"] = Relationship(back_populates="set")


class Match(_BaseModel, table=True):
    __tablename__ = "matches"
    set_id: Optional[int] = Field(default=None, foreign_key="sets.id")

    set: Optional[Set] = Relationship(back_populates="matches")


####################################################################
### SECTION 2


class Team(_BaseModel, table=True):
    __tablename__ = "teams"
    name: str


class Player(_BaseModel, table=True):
    __tablename__ = "players"
    name: str


####################################################################
### SECTION 3


class MatchInfo(_BaseModel, table=True):
    """ Contains 1 player's information about a particular match"""
    # todo: what is a better name for this?
    __tablename__ = "matchinfo"
    match_id: Optional[int] = Field(default=None, foreign_key="matches.id")
    player_id: Optional[int] = Field(default=None, foreign_key="players.id")
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
    score: int = 0
    deck_link: str
    # Todo: Let's figure out a proper representation for classes later
    #  This is a hacky middleground.
    # Todo: define with length of 4
    classes: list[str]
    ban: str














####################################################################
### LINKING TABLES


# class Linking_Team_Conference_Player(_BaseModel, table=True):
#     __tablename__ = "linking_team_conference_player"
#     team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
#     conference_id: Optional[int] = Field(default=None, foreign_key="conferences.id")
#     player_id: Optional[int] = Field(default=None, foreign_key="players.id")
#
#     team: Optional[Team] = Relationship()
#     season: Optional[Season] = Relationship()
#     player: Optional[Player] = Relationship()


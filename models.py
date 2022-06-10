# TODO: Unique indexes

from typing import Optional
from datetime import datetime as DateTime
from hearthstone.enums import CardClass
from sqlalchemy import func

from sqlmodel import SQLModel, Field, Relationship


class _BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)


# class _OneToOne(_BaseModel):
#     pass
#
#
# class _OneToMany(_BaseModel):
#     pass
#
#
# class _ManyToMany(_BaseModel):
#     pass
#
#
# class _ManyToOne(_BaseModel):
#     pass


class Season(_BaseModel, table=True):
    name: str

    series: list["Series"] = Relationship(back_populates="season")


class Series(_BaseModel, table=True):
    name: str
    season_id: Optional[int] = Field(default=None, foreign_key="season.id")

    season: Season = Relationship(back_populates="series")
    conferences: list["Conference"] = Relationship(back_populates="series")
    weeks: list["Week"] = Relationship(back_populates="series")


class Conference(_BaseModel, table=True):
    name: str
    series_id: Optional[int] = Field(default=None, foreign_key="series.id")

    series: Optional[Series] = Relationship(back_populates="conferences")


class Week(_BaseModel, table=True):
    number: int
    date: DateTime
    name: Optional[str]
    series_id: Optional[int] = Field(default=None, foreign_key="series.id")

    series: Optional[Series] = Relationship(back_populates="weeks")



class Team(_BaseModel, table=True):
    name: str


# Todo: naming?
class TeamStandings(_BaseModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    conference_id: Optional[int] = Field(default=None, foreign_key="conference.id")
    points: int
    wins: int
    losses: int
    ties: int

    teams: list[Team] = Relationship()
    conferences: list[Conference] = Relationship()

    # Calculated fields
    # ppw (points per week)
    # aos (average opponent strength)


class TeamsToMembers(_BaseModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    player_id: Optional[int] = Field(default=None, foreign_key="player.id")

    is_active: bool



class Match(_BaseModel, table=True):
    week_id: int = Field(default=None, foreign_key="week.id")

    # home_team: Optional[Team] = Relationship()
    # away_team: Optional[Team] = Relationship()
    # home_team_player: Optional["Player"] = Relationship()
    # away_team_player: Optional["Player"] = Relationship()
    teams: list["Team"] = Relationship()
    players: list["Player"] = Relationship()
    sets: list["set"] = Relationship()


class MatchToTeam(_BaseModel, table=True):
    match_id: Optional[Match] = Field(default=None, foreign_key="match.id")
    team_id: Optional[Team] = Field(default=None, foreign_key="team.id")
    is_home_team: bool


class Player(_BaseModel, table=True):
    name: str

    sets: list["Set"] = Relationship()


class Set(_BaseModel, table=True):
    match_id: int = Field(default=None, foreign_key="match.id")
    seed: int

    match: Optional[Match] = Relationship()
    players: list[Player] = Relationship()
    lineups: list["Lineup"] = Relationship()
    # home_team_player: Optional[Player] = Relationship()
    # away_team_player: Optional[Player] = Relationship()

# Todo: naming
class SetToPlayer(_BaseModel, table=True):
    set_id: Optional[int] = Field(default=None, foreign_key="set.id")
    player_id: Optional[int] = Field(default=None, foreign_key="player.id")
    is_hometeamplayer: bool
    score: int = Field(default=0)
    ban: Optional[str]

    set: Optional[Set] = Relationship()
    player: Optional[Player] = Relationship()


class Lineup(_BaseModel, table=True):
    set_id: int = Field(default=None, foreign_key="set.id")
    player_id: int = Field(default=None, foreign_key="player.id")
    d0nkey: str

    set: Optional[Set] = Relationship(back_populates="lineups")
    deck_choices: list["DeckChoice"] = Relationship(back_populates="lineup")



class DeckChoice(_BaseModel, table=True):
    lineup_id: int = Field(default=None, foreign_key="lineup.id")
    type: str
    class_: str
    deckcode: str

    lineup: Optional[Lineup] = Relationship(back_populates="deck_choices")

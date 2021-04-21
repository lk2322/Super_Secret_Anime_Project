from datetime import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

user_to_anime = sqlalchemy.Table(
    'user_to_anime',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('anime', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('animes.id'))
)


class Anime(SqlAlchemyBase):
    __tablename__ = 'animes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title_ru = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title_jp = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    release_year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.now)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.now)
    poster_path = sqlalchemy.Column(sqlalchemy.String)
    videos_path = sqlalchemy.Column(sqlalchemy.String)
    ep_col = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    dubs = orm.relation("Dubs",
                        secondary="anime_to_dubs",
                        backref="animes")
    genres = orm.relation("Genres",
                          secondary="anime_to_genres",
                          backref="animes")
    in_favorites = orm.relation("User",
                                secondary="user_to_anime",
                                backref="animes")

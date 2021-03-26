import sqlalchemy
from .db_session import SqlAlchemyBase

anime_to_genres = sqlalchemy.Table(
    'anime_to_genres',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('anime', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('animes.id')),
    sqlalchemy.Column('genre', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('genres.id'))
)


class Genres(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

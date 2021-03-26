import sqlalchemy
from .db_session import SqlAlchemyBase

anime_to_dubs = sqlalchemy.Table(
    'anime_to_dubs',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('anime', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('animes.id')),
    sqlalchemy.Column('dub', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('dubs.id'))
)


class Dubs(SqlAlchemyBase):
    __tablename__ = 'dubs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

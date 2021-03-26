import sqlalchemy
from .db_session import SqlAlchemyBase

users_to_roles = sqlalchemy.Table(
    'users_to_roles',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('role', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('roles.id'))
)


class Roles(SqlAlchemyBase):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

import sqlalchemy
from sqlalchemy_serializer import *
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Forums(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'forums'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    creators_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))

    creator = orm.relation('User')
    discussion = orm.relation("Discussions", back_populates='forum')

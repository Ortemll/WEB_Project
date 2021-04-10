import datetime
import sqlalchemy
from sqlalchemy_serializer import *
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Discussions(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'discussions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    creators_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    forum_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("forums.id"))

    creator = orm.relation('User')
    forum = orm.relation('Forums')
    messages = orm.relation("Messages", back_populates='discussion')
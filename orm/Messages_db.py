import datetime
import sqlalchemy
from sqlalchemy_serializer import *
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Messages(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creation_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    likes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    dislikes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    creators_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    discussion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("discussions.id"))

    creator = orm.relation('User')
    discussion = orm.relation('Discussions')



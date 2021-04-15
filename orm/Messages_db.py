import sqlalchemy as sql
from .db_session import SqlAlchemyBase
import datetime
from sqlalchemy import orm
from sqlalchemy_serializer import *
from flask_login import UserMixin


class Message(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'messages'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    content = sql.Column(sql.Text, nullable=False)
    likes, dislikes = sql.Column(sql.Integer, default=0), sql.Column(sql.Integer, default=0)

    # я хочу поговорить на эту тему
    answers_to_id = sql.Column(sql.Integer, sql.ForeignKey('messages.id'), nullable=True, index=True)
    # комментарий, на который отвечает данный -> Comment
    answers_to = orm.relation('Message', back_populates='answered_by', uselist=False)
    # комментарии, отвечающие на данный -> [Comment, ...]
    answered_by = orm.relation('Message', uselist=True)
    # боюсь что запутуюсь

    discussion_id = sql.Column(sql.Integer, sql.ForeignKey("discussions.id"))
    discussion = orm.relation('Discussion', back_populates='messages', uselist=False)
    user = orm.relation('User', back_populates='messages')



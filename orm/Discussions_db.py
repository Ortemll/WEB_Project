import sqlalchemy as sql
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import *
from flask_login import UserMixin


class Discussion(SqlAlchemyBase):
    __tablename__ = 'discussions'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    title = sql.Column(sql.String, nullable=False)
    # Не до конца понял для чего это
    #question_id = sql.Column(sql.Integer, sql.ForeignKey('messages.id'))
    #answer_id = sql.Column(sql.Integer, sql.ForeignKey('messages.id'), nullable=True)
    #question = orm.relation('Message', sql.ForeignKey('question_id'), uselist=False)
    #answer = orm.relation('Message', sql.ForeignKey('answer_id'), uselist=False)

    forum_id = sql.Column(sql.Integer, sql.ForeignKey("forums.id"))

    forum = orm.relation('Forum', back_populates='discussion', uselist=False)
    messages = orm.relation("Message", back_populates='discussion', uselist=True)

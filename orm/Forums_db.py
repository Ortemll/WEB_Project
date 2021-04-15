import sqlalchemy as sql
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import *
from flask_login import UserMixin


class Forum(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'forums'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    title = sql.Column(sql.String, nullable=False)
    creator_id = sql.Column(sql.String, sql.ForeignKey("users.id"))

    creator = orm.relation('User')
    discussion = orm.relation("Discussion", back_populates='forum')
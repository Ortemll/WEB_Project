from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import *
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    networks = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_lvl = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    all_forums = orm.relation("Discussions", back_populates='creator')
    all_discussions = orm.relation("Forums", back_populates='creator')
    all_messages = orm.relation("Messages", back_populates='creator')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

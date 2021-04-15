import sqlalchemy as sql
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from sqlalchemy_serializer import *
from flask_login import UserMixin


class Ban(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'banned'

    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'), primary_key=True)
    user = orm.relation('User', back_populates='ban')


class User(SqlAlchemyBase, UserMixin, SerializerMixin):

    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    unique_name = sql.Column(sql.String, index=True, unique=True, nullable=False)
    name = sql.Column(sql.String, nullable=True)
    about = sql.Column(sql.String, nullable=True)
    vk_id = sql.Column(sql.String, index=True, nullable=True, unique=True)
    hashed_password = sql.Column(sql.String, nullable=False)
    # уровни пользоввателей:
    # 0 - "высший админ"  может удалять пользователей, назначать/удалять админов и всё из 1
    # 1 - "админ"  может блокировать полизователей и удалять комментарии,
    #       создавать/удалять форумы и всё из 2
    # 2 - "пользователь"  может создавать/редактировать/удалять свои сообщения,
    #       ставить лайки и дизлайки, создавать/удалять обсуждения
    lvl = sql.Column(sql.Integer, nullable=True, default=2)
    picture = sql.Column(sql.BLOB, nullable=True)

    ban = orm.relation('Ban', back_populates='user', uselist=False)
    messages = orm.relation('Message', back_populates='user', uselist=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_ban(self, set_ban=True):
        # если set_ban == True, то пользователь блокируется, если False, то разблокируется
        self.ban = Ban(user_id=self.id) if set_ban else None

    def adding_images_to_the_db(self, file):
        with open(file, 'rb') as res:
            blob = res.read()
            return blob

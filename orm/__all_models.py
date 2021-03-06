import sqlalchemy as sql
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  UserMixin
import os


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    uniq_name = sql.Column(sql.String, index=True, unique=True, nullable=False)
    name = sql.Column(sql.String, nullable=True)
    about = sql.Column(sql.Text, nullable=True)
    vk_id = sql.Column(sql.String, index=True, nullable=True)
    hashed_password = sql.Column(sql.String, nullable=False)
    is_banned = sql.Column(sql.Boolean, default=False)

    with open(fr'{os.getcwd()}\static\img\default_image.jpg', 'rb') as picture:
        blob_data = picture.read()
    profile_picture = sql.Column(sql.BLOB,
                                 default=blob_data,
                                 nullable=True)
    profile_picture_name = sql.Column(sql.String, default='default_image.jpg', nullable=True)

    # уровни пользоввателей:
    # 0 - "высший админ"  может удалять пользователей, назначать/удалять админов и всё из 1
    # 1 - "админ"  может блокировать полизователей и удалять комментарии и обсуждения,
    #       создавать/удалять форумы и всё из 2
    # 2 - "пользователь"  может создавать/редактировать/удалять свои сообщения,
    #       ставить лайки и дизлайки, создавать/удалять свои обсуждения
    lvl = sql.Column(sql.Integer, nullable=False, default=2)

    messages = orm.relation('Message', back_populates='user', uselist=True)
    forums = orm.relation('Forum', back_populates='creator', uselist=True)
    discussions = orm.relation('Discussion', back_populates='creator', uselist=True)

    liked = orm.relation('Message', secondary='association_like', backref='liked_by')
    disliked = orm.relation('Message', secondary='association_dislike', backref='disliked_by')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def write_to_file(self, name, filename):
        with open(filename, 'wb') as file:
            file.write(name)

    def conver_to_binary(self, file):
        with open(file, 'rb') as picture:
            blob_data = picture.read()
        return blob_data

class Message(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'messages'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    user_id = sql.Column(sql.Integer, sql.ForeignKey(User.id))
    content = sql.Column(sql.Text, nullable=False)
    likes, dislikes = sql.Column(sql.Integer, default=0), sql.Column(sql.Integer, default=0)
    answers_to_id = sql.Column(sql.Integer, sql.ForeignKey('messages.id'), nullable=True, index=True)
    discussion_id = sql.Column(sql.Integer, sql.ForeignKey("discussions.id"), nullable=False)

    discussion = orm.relation('Discussion', back_populates='messages', uselist=False)
    user = orm.relation('User', back_populates='messages')


class Discussion(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'discussions'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    title = sql.Column(sql.String, nullable=False)
    forum_id = sql.Column(sql.Integer, sql.ForeignKey("forums.id"), nullable=False)
    creator_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"), nullable=False)

    creator = orm.relation('User', back_populates='discussions', uselist=False)
    forum = orm.relation('Forum', back_populates='discussions', uselist=False)
    messages = orm.relation("Message", back_populates='discussion', uselist=True)


class Forum(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'forums'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    title = sql.Column(sql.String, nullable=False)
    creator_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"), nullable=False)

    creator = orm.relation('User', back_populates='forums', uselist=False)
    discussions = orm.relation("Discussion", back_populates='forum', uselist=True)


association_like_table = sql.Table('association_like',
    SqlAlchemyBase.metadata,
    sql.Column('message', sql.Integer,
                      sql.ForeignKey('messages.id')),
    sql.Column('user', sql.Integer,
                      sql.ForeignKey('users.id')))

association_dislike_table = sql.Table('association_dislike',
    SqlAlchemyBase.metadata,
    sql.Column('message', sql.Integer,
                      sql.ForeignKey('messages.id')),
    sql.Column('user', sql.Integer,
                      sql.ForeignKey('users.id')))
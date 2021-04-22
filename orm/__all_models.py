import sqlalchemy as sql
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    uniq_name = sql.Column(sql.String, index=True, unique=True, nullable=False)
    name = sql.Column(sql.String, nullable=True)
    about = sql.Column(sql.Text, nullable=True)
    vk_id = sql.Column(sql.String, index=True, nullable=True, unique=True)
    hashed_password = sql.Column(sql.String, nullable=False)
    # уровни пользоввателей:
    # 0 - "высший админ"  может удалять пользователей, назначать/удалять админов и всё из 1
    # 1 - "админ"  может блокировать полизователей и удалять комментарии и обсуждения,
    #       создавать/удалять форумы и всё из 2
    # 2 - "пользователь"  может создавать/редактировать/удалять свои сообщения,
    #       ставить лайки и дизлайки, создавать/удалять свои обсуждения
    lvl = sql.Column(sql.Integer, nullable=False, default=2)
    profile_picture = sql.Column(sql.BLOB, nullable=True)

    ban = orm.relation('Ban', back_populates='user', uselist=False)
    messages = orm.relation('Message', back_populates='user', uselist=True)
    forums = orm.relation('Forum', back_populates='creator', uselist=True)
    discussions = orm.relation('Discussion', back_populates='creator', uselist=True)

    # liked = orm.relation('Discussion', foreign_keys='[Mu.assigned_to]', uselist=True)
    # disliked = orm.relation('Discussion', foreign_keys='[Tasks.assigned_to]', uselist=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_ban(self, set_ban=True):
        # если set_ban == True, то пользователь блокируется, если False, то разблокируется
        self.ban = Ban(user_id=self.id) if set_ban else None

    def set_profile_picture(self, file):
        with open(file, 'rb') as picture:
            self.profile_picture = picture.read()

class Ban(SqlAlchemyBase):
    __tablename__ = 'banned'

    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'), primary_key=True)
    user = orm.relation('User', back_populates='ban')


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    user_id = sql.Column(sql.Integer, sql.ForeignKey(User.id), nullable=False)
    content = sql.Column(sql.Text, nullable=False)
    likes, dislikes = sql.Column(sql.Integer, default=0), sql.Column(sql.Integer, default=0)
    answers_to_id = sql.Column(sql.Integer, sql.ForeignKey('messages.id'), nullable=True, index=True)
    discussion_id = sql.Column(sql.Integer, sql.ForeignKey("discussions.id"), nullable=False)

    discussion = orm.relation('Discussion', back_populates='messages', uselist=False)
    user = orm.relation('User', back_populates='messages')


class Discussion(SqlAlchemyBase):
    __tablename__ = 'discussions'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    title = sql.Column(sql.String, nullable=False)
    forum_id = sql.Column(sql.Integer, sql.ForeignKey("forums.id"), nullable=False)
    creator_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"), nullable=False)

    creator = orm.relation('User', back_populates='discussions', uselist=False)
    forum = orm.relation('Forum', back_populates='discussions', uselist=False)
    messages = orm.relation("Message", back_populates='discussion', uselist=True)


class Forum(SqlAlchemyBase):
    __tablename__ = 'forums'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    title = sql.Column(sql.String, nullable=False)
    creator_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"), nullable=False)

    creator = orm.relation('User', back_populates='forums', uselist=False)
    discussions = orm.relation("Discussion", back_populates='forum', uselist=True)


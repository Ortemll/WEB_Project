from flask import *

from orm import db_session
from orm.__all_models import *
from flask_restful import abort, Resource
import parser_for_user as parser_us
import parser_for_forum as parser_fr
import parser_for_message as parser_ms
import requests


def User_not_found(user_id):
    if not str(user_id).isdigit():
        abort(404, error=f"{user_id} not int")
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404, error=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        User_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(user_id)

        return jsonify({'user': users.to_dict(
            only=('name', 'about', 'lvl', 'is_banned'))})

    def delete(self, user_id):
        User_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        for i in db_sess.query(User).filter(User.forums).all():
            for j in i.forums:
                for k in j.discussions:
                    for p in k.messages:
                        db_sess.delete(p)
                    db_sess.delete(k)
                db_sess.delete(j)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'user': [item.to_dict(only=('name', 'about', 'lvl', 'is_banned')) for item in users]})

    def post(self):
        if not request.json:
            return jsonify({'error': 'Empty request'})
        db_sess = db_session.create_session()
        a = ['uniq_name', 'lvl', 'is_banned', 'password']
        for i in a:
            if i not in request.json:
                return jsonify({'error': 'Bad info'})
        if db_sess.query(User).filter(request.json['uniq_name'] == User.uniq_name).first():
            return jsonify({'error': 'Пользователь с таким uniq_name уже есть'})
        if db_sess.query(User).filter(request.json['vk_id'] == User.vk_id).first():
            return jsonify({'error': 'Пользователь с таким vk_id уже есть'})
        if request.json['vk_id'].isdigit():
            vk_id = requests.get(f'https://vk.com/id{request.json["vk_id"]}')
        else:
            vk_id = requests.get(f'https://vk.com/{request.json["vk_id"]}')
        if not vk_id:
            return jsonify({'error': 'Пользователь с таким vk_id нет'})
        password = generate_password_hash(request.json['password'])
        request.json['password'] = password
        args = parser_us.parse_args()
        user = User(
            uniq_name=args['uniq_name'],
            name=args['name'],
            about=args['about'],
            vk_id=args['vk_id'],
            lvl=args['lvl'],
            is_banned=args['is_banned'],
            hashed_password=args['password']
        )
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def Forum_not_found(forum_id):
    if not str(forum_id).isdigit():
        abort(404, error=f"{forum_id} not int")
    db_sess = db_session.create_session()
    forum = db_sess.query(User).get(forum_id)
    if not forum or forum is None:
        abort(404, error=f"Forum {forum_id} not found")


class ForumResource(Resource):
    def get(self, forum_id):
        Forum_not_found(forum_id)
        db_sess = db_session.create_session()
        forum = db_sess.query(Forum).get(forum_id)
        if not forum or forum is None:
            abort(404, error=f"Forum {forum_id} not found")
        return jsonify({'forum': forum.to_dict(only=('title', 'creator_id'))})

    def delete(self, forum_id):
        Forum_not_found(forum_id)
        db_sess = db_session.create_session()
        forum = db_sess.query(Forum).get(forum_id)
        if not forum or forum is None:
            abort(404, error=f"Forum {forum_id} not found")
        for j in db_sess.query(Forum).filter(forum.discussions).all():
            for z in j.messages:
                db_sess.delete(z)
            db_sess.delete(j)
        db_sess.delete(forum)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class ForumsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        forums = db_sess.query(Forum).all()
        return jsonify({'forum': [item.to_dict(only=('title', 'creator_id')) for item in forums]})

    def post(self):
        if not request.json:
            return jsonify({'error': 'Empty request'})
        args = parser_fr.parse_args()
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(request.json['creator_id'] == User.id).first():
            return jsonify({'error': 'user not found'})
        forum = Forum(
            title=args['title'],
            creator_id=args['creator_id'],
        )
        db_sess.add(forum)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def Discussion_not_found(discussion_id):
    if not str(discussion_id).isdigit():
        abort(404, error=f"{discussion_id} not int")
    db_sess = db_session.create_session()
    discussion = db_sess.query(Discussion).get(discussion_id)
    if not discussion:
        abort(404, error=f"Discussion {discussion_id} not found")


class DiscussionResource(Resource):
    def get(self, discussion_id):
        Discussion_not_found(discussion_id)
        db_sess = db_session.create_session()
        discussion = db_sess.query(Discussion).get(discussion_id)
        return jsonify({'discussion': discussion.to_dict(
            only=('title', 'forum_id', 'creator_id'))})

    def delete(self, discussion_id):
        Discussion_not_found(discussion_id)
        db_sess = db_session.create_session()
        discussion = db_sess.query(Discussion).get(discussion_id)
        for j in db_sess.query(Discussion).filter(discussion.messages).all():
            db_sess.delete(j)
        db_sess.delete(discussion)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class DiscussionsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        discussions = db_sess.query(Discussion).all()
        return jsonify({'discussion': [item.to_dict(
            only=('title', 'creator_id')) for item in discussions]})

    def post(self):
        if not request.json:
            return jsonify({'error': 'Empty request'})
        args = parser_fr.parse_args()
        db_sess = db_session.create_session()
        a = ['title', 'forum_id', 'creator_id']
        for i in a:
            if i not in request.json:
                return jsonify({'error': 'Bad info'})
            elif len(request.json.values()) != len(a):
                return jsonify({'error': 'Bad info'})
        if not db_sess.query(Forum).filter(request.json['forum_id'] == Forum.id).first():
            return jsonify({'error': 'user not found'})
        if not db_sess.query(User).filter(request.json['creator_id'] == User.id).first():
            return jsonify({'error': 'user not found'})
        discussion = Discussion(
            title=args['title'],
            forum_id=args['forum_id'],
            creator_id=args['creator_id']

        )
        db_sess.add(discussion)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def Message_not_found(message_id):
    if not str(message_id).isdigit():
        abort(404, error=f"{message_id} not int")
    db_sess = db_session.create_session()
    message = db_sess.query(Message).get(message_id)
    if not message:
        abort(404, error=f"Message {message_id} not found")


class MessageResource(Resource):
    def get(self, message_id):
        Message_not_found(message_id)
        db_sess = db_session.create_session()
        message = db_sess.query(Message).get(message_id)

        return jsonify({'message': message.to_dict(
            only=('user_id', 'content', 'answers_to_id', 'discussion_id'))})

    def delete(self, message_id):
        Message_not_found(message_id)
        db_sess = db_session.create_session()
        message = db_sess.query(Message).get(message_id).first()
        db_sess.delete(message)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class MessagesListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        messages = db_sess.query(Message).all()
        return jsonify({'message': [item.to_dict(
            only=('surname', 'name', 'age', 'position')) for item in messages]})

    def post(self):
        if not request.json:
            return jsonify({'error': 'Empty request'})
        args = parser_ms.parse_args()
        db_sess = db_session.create_session()
        a = ['user_id', 'content', 'answers_to_id', 'discussion_id']
        for i in a:
            if i not in request.json:
                return jsonify({'error': 'Bad info'})
            elif len(request.json.values()) != len(a):
                return jsonify({'error': 'Bad info'})
        if not db_sess.query(Discussion).filter(request.json['discussion_id'] == Discussion.id).first():
            return jsonify({'error': 'Discussion not found'})
        if not db_sess.query(User).filter(request.json['user_id'] == User.id).first():
            return jsonify({'error': 'user not found'})
        if not db_sess.query(User).filter(request.json['answers_to_id'] == User.id).first():
            return jsonify({'error': 'responds to not found'})
        message = Message(
            user_id=args['user_id'],
            content=args['content'],
            answers_to_id=args['answers_to_id'],
            discussion_id=args['discussion_id'],
        )
        db_sess.add(message)
        db_sess.commit()
        return jsonify({'success': 'OK'})

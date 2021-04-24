from flask import *

from orm import db_session
from orm.__all_models import *
from flask_restful import abort, Resource
import parser_for_user as parser_us
import parser_for_forum as parser_fr
import parser_for_message as parser_ms
import parser_for_discussion as parser_ds
from flask import make_response


def User_not_found(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


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
        for i in db_sess.query(User).all(user.forums):
            for j in db_sess.query(Forum).all(i.discussions):
                for z in db_sess.query(Discussion).all(j.messages):
                    db_sess.delete(z)
                db_sess.delete(j)
            db_sess.delete(i)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'user': [item.to_dict(only=('name', 'about', 'lvl', 'is_banned')) for item in users]})

    def post(self):
        args = parser_us.parse_args()
        db_sess = db_session.create_session()
        user = User(
            uniq_name=args['uniq_name'],
            name=args['name'],
            about=args['about'],
            vk_id_str=args['vk_id_str'],
            vk_id_int=args['vk_id_int'],
            lvl=args['lvl'],
            is_banned=args['is_banned']
        )
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def Forum_not_found(forum_id):
    db_sess = db_session.create_session()
    forum = db_sess.query(User).get(forum_id)
    if not forum:
        abort(404, message=f"Forum {forum_id} not found")


class ForumResource(Resource):
    def get(self, forum_id):
        Forum_not_found(forum_id)
        db_sess = db_session.create_session()
        forum = db_sess.query(Forum).get(forum_id)
        return jsonify({'forum': forum.to_dict(
            only=('title', 'creator_id'))})

    def delete(self, forum_id):
        Forum_not_found(forum_id)
        db_sess = db_session.create_session()
        forum = db_sess.query(Forum).get(forum_id)
        for j in db_sess.query(Forum).all(forum.discussions):
            for z in db_sess.query(Discussion).all(j.messages):
                db_sess.delete(z)
            db_sess.delete(j)
        db_sess.delete(forum)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class ForumsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        forums = db_sess.query(Forum).all()
        return jsonify({'forum': [item.to_dict(
            only=('title', 'creator_id')) for item in forums]})

    def post(self):
        args = parser_fr.parse_args()
        db_sess = db_session.create_session()
        forum = Forum(
            title=args['title'],
            creator_id=args['creator_id'],
        )
        db_sess.add(forum)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def Discussion_not_found(discussion_id):
    db_sess = db_session.create_session()
    discussion = db_sess.query(Discussion).get(discussion_id)
    if not discussion:
        abort(404, message=f"Discussion {discussion_id} not found")


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
        for j in db_sess.query(Discussion).all(discussion.messages):
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
        args = parser_fr.parse_args()
        db_sess = db_session.create_session()
        discussion = Discussion(
            title=args['title'],
            forum_id=args['forum_id'],
            creator_id=args['creator_id']

        )
        db_sess.add(discussion)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def Message_not_found(message_id):
    db_sess = db_session.create_session()
    message = db_sess.query(Message).get(message_id)
    if not message:
        abort(404, message=f"Users {message_id} not found")


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
        message = db_sess.query(Message).get(message_id)
        db_sess.delete(message)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class MessagesListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        messages = session.query(Message).all()
        return jsonify({'message': [item.to_dict(
            only=('surname', 'name', 'age', 'position')) for item in messages]})

    def post(self):
        args = parser_ms.parse_args()
        db_sess = db_session.create_session()
        message = Message(
            user_id=args['user_id'],
            content=args['content'],
            answers_to_id=args['answers_to_id'],
            discussion_id=args['discussion_id'],
        )
        db_sess.add(message)
        db_sess.commit()
        return jsonify({'success': 'OK'})

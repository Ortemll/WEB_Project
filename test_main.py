from requests import get, put, post, delete
from time import sleep
import json

print(get('http://127.0.0.1:5000/api/user/1').json())
print(get('http://127.0.0.1:5000/api/user/10000').json())
print(get('http://127.0.0.1:5000/api/user/q').json())

print(delete('http://127.0.0.1:5000/api/user/1').json())
print(delete('http://127.0.0.1:5000/api/user/10000').json())
print(delete('http://127.0.0.1:5000/api/user/q').json())

print(get('http://127.0.0.1:5000/api/users').json())
print(get('http://127.0.0.1:5000/api/userssssss').json())

print(post('http://127.0.0.1:5000/api/users', json={'uniq_name': 'name', 'name': 'name',
                                                    'about': 'about', 'vk_id': '', 'lvl': 0,
                                                    'is_banned': 0, 'password':'123123'}).json())
print(post('http://127.0.0.1:5000/api/users', json={'a': 'title_2', 'creator_id': 10000}).json())
print(post('http://127.0.0.1:5000/api/usersg', json={'title': 'title_3', 'creator_id': 1}).json())

print(get('http://127.0.0.1:5000/api/forum/1').json())
print(get('http://127.0.0.1:5000/api/forum/10000').json())
print(get('http://127.0.0.1:5000/api/forum/q').json())

print(delete('http://127.0.0.1:5000/api/forum/1').json())
print(delete('http://127.0.0.1:5000/api/forum/10000').json())
print(delete('http://127.0.0.1:5000/api/forum/q').json())

print(get('http://127.0.0.1:5000/api/forums').json())
print(get('http://127.0.0.1:5000/api/forumssssss').json())

print(post('http://127.0.0.1:5000/api/forums', json={'title': 'title', 'creator_id': 1}).json())
print(post('http://127.0.0.1:5000/api/forums', json={'a': 'title_2', 'creator_id': 10000}).json())
print(post('http://127.0.0.1:5000/api/forumssg', json={'title': 'title_3', 'creator_id': 1}).json())

print(get('http://127.0.0.1:5000/api/discussion/1').json())
print(get('http://127.0.0.1:5000/api/discussion/10000').json())
print(get('http://127.0.0.1:5000/api/discussion/q').json())

print(delete('http://127.0.0.1:5000/api/discussion/1').json())
print(delete('http://127.0.0.1:5000/api/discussion/10000').json())
print(delete('http://127.0.0.1:5000/api/discussion/q').json())

print(get('http://127.0.0.1:5000/api/discussions').json())
print(get('http://127.0.0.1:5000/api/discussionssssss').json())

print(post('http://127.0.0.1:5000/api/discussions', json={'title': 'title', 'creator_id': 1}).json())
print(post('http://127.0.0.1:5000/api/discussions', json={'a': 'title_2', 'creator_id': 10000}).json())
print(post('http://127.0.0.1:5000/api/discussionsg', json={'title': 'title_3', 'creator_id': 1}).json())

print(get('http://127.0.0.1:5000/api/message/1').json())
print(get('http://127.0.0.1:5000/api/message/10000').json())
print(get('http://127.0.0.1:5000/api/message/q').json())

print(delete('http://127.0.0.1:5000/api/message/1').json())
print(delete('http://127.0.0.1:5000/api/message/10000').json())
print(delete('http://127.0.0.1:5000/api/message/q').json())

print(get('http://127.0.0.1:5000/api/messages').json())
print(get('http://127.0.0.1:5000/api/umessagessss').json())

print(post('http://127.0.0.1:5000/api/messages', json={'title': 'title', 'creator_id': 1}).json())
print(post('http://127.0.0.1:5000/api/messages', json={'a': 'title_2', 'creator_id': 10000}).json())
print(post('http://127.0.0.1:5000/api/messagesg', json={'title': 'title_3', 'creator_id': 1}).json())

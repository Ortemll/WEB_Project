from requests import get, put, post, delete
from time import sleep
print(get('http://127.0.0.1:5000/api/users').json())

print(get('http://127.0.0.1:5000/api/user/1').json())

print(get('http://localhost:5000/api/forums').json())
print(get('http://localhost:5000/api/forum/<int:forum_id>').json())

print(get('http://localhost:5000/api/messages').json())
print(get('http://localhost:5000/api/message/<int:message_id>').json())

print(get('http://localhost:5000/api/discussions').json())
print(get('http://localhost:5000/api/discussion/<int:discussion_id>').json())

print(post('http://localhost:8080/api/v2/users',
           json={'surname': 'surname', 'name': 'name', 'age': 20, 'position': 'pos_1'}))

print(delete('http://localhost:5000/api/v2/users/999').json())

print(delete('http://localhost:5000/api/v2/users/1').json())


print(get('http://localhost:5000/api/v2/users').json())

print(get('http://localhost:5000/api/v2/users/999').json())

print(post('http://localhost:5000/api/v2/users',
           json={'id': 100}).json())


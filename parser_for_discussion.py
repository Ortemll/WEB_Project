from flask_restful import reqparse

def parse_args():
    parser = reqparse.RequestParser()
    parser.add_argument('title', required=True, type=str)
    parser.add_argument('forum_id', required=True, type=int)
    parser.add_argument('creator_id', required=True, type=int)
    a = parser.parse_args()
    return a
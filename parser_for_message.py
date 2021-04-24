from flask_restful import reqparse

def parse_args():
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, type=str)
    parser.add_argument('content', required=True, type=str)
    parser.add_argument('answers_to_id', required=True, type=int)
    parser.add_argument('discussion_id', required=True, type=str)
    a = parser.parse_args()
    return a
from flask_restful import reqparse

def parse_args():
    parser = reqparse.RequestParser()
    parser.add_argument('uniq_name', required=True, type=str)
    parser.add_argument('name', required=False, type=str)
    parser.add_argument('about', required=False, type=str)
    parser.add_argument('vk_id_str', required=False, type=str)# если не правильно то выводит ошибку
    parser.add_argument('vk_id_int', required=False, type=int)# если не правильно то выводит ошибку
    parser.add_argument('lvl', required=True, type=int)# если не правильно то выводит ошибку
    parser.add_argument('is_banned', required=True, type=bool)
    a = parser.parse_args()
    return a

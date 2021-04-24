from flask_restful import reqparse
from orm.__all_models import *
import requests


def parse_args():
    parser = reqparse.RequestParser()
    parser.add_argument('uniq_name', required=True, type=str)
    parser.add_argument('name', required=False, type=str)
    parser.add_argument('about', required=False, type=str)
    parser.add_argument('vk_id', required=False, type=str)
    parser.add_argument('lvl', required=True, type=int)
    parser.add_argument('is_banned', required=True, type=bool)
    parser.add_argument('password', required=True, type=str)
    a = parser.parse_args()
    return a

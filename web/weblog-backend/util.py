import re
import secrets

import psycopg2 as psycopg2
import jwt
from datetime import datetime, timedelta

from res import *

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
SECRET_KEY = secrets.token_hex()
tokens = {}


class UserTokenExpiredError(Exception):
    """Exception raised when user token expires."""

    def __init__(self, message="Session has expired"):
        self.message = message
        super().__init__(self.message)


class BadAuthorizationToken(Exception):
    """Exception raised when user token expires."""

    def __init__(self, message="User auth header does not match the user id"):
        self.message = message
        super().__init__(self.message)


def get_token(req):
    token = req.headers.get('Authorization')
    if token:
        token = token.split(' ')[1]
    else:
        token = ''
    return token


def get_current_user(token):
    return jwt.decode(token, SECRET_KEY, algorithms="HS256")['user_id']


def is_user_not_signed_in(user_id, token, is_not_get=True, is_not_comment=True):
    if not is_not_get:
        return False

    uuid_exp = jwt.decode(token, SECRET_KEY, algorithms="HS256")

    if (not user_id) and (not token) and (not user_id) in (not tokens) and (not tokens[user_id]):
        raise BadAuthorizationToken
    elif datetime.fromtimestamp(uuid_exp['exp']) - timedelta(minutes=60) < datetime.utcnow():
        raise UserTokenExpiredError
    elif not is_not_comment or user_id == uuid_exp['user_id']:
        return False
    return True


def process_json(req):
    content_type = req.headers.get('Content-Type')
    if 'application/json' in content_type:
        return req.json
    else:
        return None


def prepare_comment_resp(comments):
    if len(comments) == 0:
        res = '[]'
    elif len(comments) == 1:

        res = '[{\n' \
              '"id": "' + str(comments[-1][0]) + '",\n'

        res += '"content": "' + str(comments[-1][1]) + '"\n' \
                                                       '}]'

    else:
        res = '[\n'
        for comment in comments[:-1]:
            res += '{\n' \
                   '"id": "' + str(comment[0]) + '",\n'

            res += '"content": "' + str(comment[1]) + '"\n' \
                                                      '},\n'

        res += '{\n' \
               '"id": "' + str(comments[-1][0]) + '",\n'

        res += '"content": "' + str(comments[-1][1]) + '"\n' \
                                                       '}\n'
        res += '\n]'
    return res


def prepare_post_resp(posts):
    if len(posts) == 0:
        res = '[]'
    elif len(posts) == 1:

        res = '[{\n' \
              '"id": "' + str(posts[-1][0]) + '",\n'

        res += '"title": "' + str(posts[-1][1]) + '",\n'

        res += '"content": "' + str(posts[-1][2]) + '"\n' \
                                                    '}]'

    else:
        res = '[\n'
        for post in posts[:-1]:
            res += '{\n' \
                   '"id": "' + str(post[0]) + '",\n'

            res += '"title": "' + str(post[1]) + '",\n'

            res += '"content": "' + str(post[2]) + '"\n' \
                                                   '},\n'

        res += '{\n' \
               '"id": "' + str(posts[-1][0]) + '",\n'

        res += '"title": "' + str(posts[-1][1]) + '",\n'

        res += '"content": "' + str(posts[-1][2]) + '"\n' \
                                                    '}\n'
        res += '\n]'
    return res


def get_conn():
    return psycopg2.connect(host=host,
                            database=db_db,
                            user=db_user,
                            password=db_password)


def check_email(email):
    if re.search(EMAIL_REGEX, email):
        return True
    else:
        return False


def lower_upper_num(password):
    digit = False
    upper = False
    lower = False
    for char in password:
        if str(char).isdigit():
            digit = True
        elif str(char).isupper():
            upper = True
        elif str(char).islower():
            lower = True

    return lower and upper and digit


def check_password(password):
    if 6 <= len(password) <= 20:  # and lower_upper_num(password):
        return True
    else:
        return False

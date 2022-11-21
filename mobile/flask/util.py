import re
import secrets

import psycopg2 as psycopg2
import jwt
from datetime import datetime, timedelta
from res import *


class UserTokenExpiredError(Exception):
    """Exception raised when user token expires."""

    def __init__(self, message="User token has expired"):
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


def is_user_not_signed_in(user_id, token):
    uuid_exp = jwt.decode(token, SECRET_KEY, algorithms="HS256")

    if (not user_id) or (not token) or (not tokens) or (not tokens[user_id] == token):
        raise BadAuthorizationToken

    elif datetime.fromtimestamp(uuid_exp['exp']) - timedelta(minutes=60) < datetime.utcnow():
        tokens[user_id] = None
        raise UserTokenExpiredError

    elif user_id == uuid_exp['user_id']:
        return False

    return True


def process_json(req):
    content_type = req.headers.get('Content-Type')
    if 'application/json' in content_type:
        return req.json
    else:
        return None


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


def get_current_user(token):
    return jwt.decode(token, SECRET_KEY, algorithms="HS256")['user_id']


def get_conn():
    return psycopg2.connect(host=host,
                            database=db_db,
                            user=db_user,
                            password=db_password)


## Utils
def check_email(email):
    if re.search(EMAIL_REGEX, email):
        return True
    else:
        return False


def check_password(password):
    if 6 <= len(password) <= 20:  # and lower_upper_num(password):
        return True
    else:
        return False

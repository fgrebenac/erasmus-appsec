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

    if is_admin_user(get_current_user(token)):
        return False

    return True


def is_admin_user(uuid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT is_admin '
                'FROM app_user u '
                'WHERE id = %(uuid)s',
                {
                    "uuid": uuid
                })
    result = cur.fetchone()

    print(result[0])

    cur.close()
    conn.close()

    return result[0]


def process_json(req):
    content_type = req.headers.get('Content-Type')
    if 'application/json' in content_type:
        return req.json
    else:
        return None


def prepare_comment_resp(comments):
    if len(comments) == 0:
        res = '[]'
    else:
        res = '[\n'
        for comment in comments[:-1]:
            res += '{\n' \
                   '"id": "' + str(comment[0]) + '",\n'

            res += '"content": "' + str(comments[-1][1]) + '",\n'

            res += '"user_id": "' + str(comments[-1][2]) + '",'

            res += '"post_id": "' + str(comments[-1][3]) + '",'

            res += '"username": "' + str(comments[-1][4]) + '"' \
                                                            '},'

        res += '{\n' \
               '"id": "' + str(comments[-1][0]) + '",\n'

        res += '"content": "' + str(comments[-1][1]) + '",\n'

        res += '"user_id": "' + str(comments[-1][2]) + '",'

        res += '"post_id": "' + str(comments[-1][3]) + '",'
        res += '"username": "' + str(comments[-1][4]) + '"' \
                                                        '}'
        res += '\n]'
    return res


def prepare_post_resp(posts):
    if len(posts) == 0:
        res = '[]'
    else:
        res = '[\n'
        for post in posts[:-1]:
            res += '{\n' \
                   '"id": "' + str(post[0]) + '",\n'

            res += '"title": "' + str(post[1]) + '",\n'

            res += '"content": "' + str(post[2]) + '",\n'

            res += '"username": "' + str(post[3]) + '",\n'

            res += '"user_id": "' + str(post[4]) + '"\n' \
                                                   '},\n'

        res += '{\n' \
               '"id": "' + str(posts[-1][0]) + '",\n'

        res += '"title": "' + str(posts[-1][1]) + '",\n'

        res += '"content": "' + str(posts[-1][2]) + '",\n'

        res += '"username": "' + str(posts[-1][3]) + '",\n'

        res += '"user_id": "' + str(posts[-1][4]) + '"\n' \
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


def check_password(password):
    if 6 <= len(password) <= 20:
        return True
    else:
        return False

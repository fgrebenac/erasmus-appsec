from datetime import datetime, timedelta

import jwt
from flask import Flask, request, Response
from util import *
import bcrypt
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/login", methods=['POST'])
@cross_origin()
def login():
    try:
        conn = get_conn()
        json_body = process_json(request)
        username = json_body['username']
        password = json_body['password']

        cur = conn.cursor()
        cur.execute('SELECT id, password FROM app_user '
                    "WHERE username = %(username)s",
                    {
                        'username': username
                    })  # to avoid string encoding error

        user = cur.fetchone()
        cur.close()
        conn.close()
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, SECRET_KEY)

        tokens[user[0]] = token

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return Response('{'
                        '   "error": "' + str(error) + '"'
                                                       '}',
                        status=400,
                        mimetype='application/json')

    if bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        return Response('{'
                        '  "id": "' + user[0] +
                        '",\n  "jwt": "' + token +
                        '"\n}',
                        status=200,
                        mimetype='application/json')
    else:
        return Response('{'
                        '   "error": "User/Pass don\'t exist"'
                        '}',
                        status=400,
                        mimetype='application/json')


@app.route("/user", methods=['POST'])
@cross_origin()
def create_user():
    try:
        json_body = process_json(request)
        password = json_body['password'].encode('utf-8')
        username = json_body['username']
        email = json_body['email']

        if not check_email(email):
            return Response('E-mail is not properly formatted', 400, mimetype='application/json')
        if not check_password(password):
            return Response('Password length should be greater than 6 and lower than 20'
                            ' and need to have at least one number and one letter', 400, mimetype='application'
                                                                                                  '/json')

        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        conn = get_conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO app_user (username, password, email) '
                    'values (%s, %s, %s)',
                    (username, hashed_pw.decode('utf-8'), email))

        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return Response('{'
                        '   "error": "' + str(error) + '"'
                                                       '}',
                        status=400,
                        mimetype='application/json')

    return Response('',
                    status=200,
                    mimetype='application/json')


@app.route("/user/<user_id>", methods=['DELETE'])
@cross_origin()
def delete_user(user_id):
    try:
        token = get_token(request)

        if is_user_not_signed_in(user_id, token):
            return Response('{'
                            '   Token does not match the user id'
                            '}', 401)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM app_user '
                    'WHERE id = %(user_id)s',
                    {
                        "user_id": get_current_user(token)
                    })

        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return Response('{'
                        '   "error": "' + str(error) + '"'
                                                       '}',
                        status=400,
                        mimetype='application/json')

    return Response('',
                    status=200,
                    mimetype='application/json')


@app.route("/user/<user_id>/post", methods=['POST'])
@cross_origin()
def create_post(user_id):
    try:
        json_body = process_json(request)

        title = json_body['title']
        content = json_body['content']
        token = get_token(request)

        if is_user_not_signed_in(user_id, token):
            return Response('{'
                            '   Token does not match the user id'
                            '}', 401)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO post (title, content, user_id)'
                    'values (%s, %s, %s)',
                    (title, content, get_current_user(token)))

        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return Response('{'
                        '   "error": "' + str(error) + '"'
                                                       '}',
                        status=400,
                        mimetype='application/json')

    return Response('',
                    status=200,
                    mimetype='application/json')


@app.route("/user/<user_id>/post", methods=['GET'])
@cross_origin()
def get_posts(user_id):
    try:
        token = get_token(request)

        if is_user_not_signed_in(user_id, token):
            return Response('{'
                            '   Token does not match the user id'
                            '}', 401)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT p.id, p.title, p.content, u.username, p.user_id FROM post p '
                    'JOIN app_user u on u.id = p.user_id '
                    'WHERE user_id = %(user_id)s',
                    {
                        'user_id': get_current_user(token)
                    })

        posts = cur.fetchall()

        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return Response('{'
                        '   "error": "' + str(error) + '"'
                                                       '}',
                        status=400,
                        mimetype='application/json')

    return Response(prepare_post_resp(posts),
                    status=200,
                    mimetype='application/json')


@app.route("/user/<user_id>/post/<post_id>", methods=['GET'])
@cross_origin()
def get_post_by_id(user_id, post_id):
    try:
        token = get_token(request)
        if is_user_not_signed_in(user_id, token):
            return Response('{'
                            '   Token does not match the user id'
                            '}', 401)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT id, title, content FROM post p '
                    'WHERE id = %s and user_id = %s',
                    (post_id, get_current_user(token)))

        posts = cur.fetchmany()

        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return Response('{'
                        '   "error": "' + str(error) + '"'
                                                       '}',
                        status=400,
                        mimetype='application/json')
    if len(posts) == 0:
        return Response('{'
                        '   "error": "post does not exist"'
                        '}',
                        status=400,
                        mimetype='application/json')

    else:
        return Response(prepare_post_resp(posts)[1:-1],
                        status=200,
                        mimetype='application/json')


@app.route("/user/<user_id>/post/<post_id>", methods=['PUT'])
@cross_origin()
def modify_post_by_id(user_id, post_id):
    try:
        json_body = process_json(request)
        title = json_body['title']
        content = json_body['content']
        token = get_token(request)

        if is_user_not_signed_in(user_id, token):
            return Response('{'
                            '   Token does not match the user id'
                            '}', 401)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute('UPDATE post SET title = %s, content = %s '
                    'WHERE id = %s and user_id = %s',
                    (title, content, post_id, get_current_user(token)))
        conn.commit()
        cur.close()
        conn.close()


    except (Exception, psycopg2.DatabaseError) as error:
        return Response('{'
                        '   "error": "' + str(error) + '"'
                                                       '}',
                        status=400,
                        mimetype='application/json')

    return Response('', status=200, mimetype='application/json')


@app.route("/user/<user_id>/post/<post_id>", methods=['DELETE'])
@cross_origin()
def delete_post_by_id(user_id, post_id):
    try:
        token = get_token(request)
        if is_user_not_signed_in(user_id, token):
            return Response('{'
                            '   Token does not match the user id'
                            '}', 401)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM post '
                    'where id = %s and user_id = %s',
                    (post_id, get_current_user(token)))

        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return Response('{'
                        '   "error": "' + str(error) + '"'
                                                       '}',
                        status=400,
                        mimetype='application/json')

    return Response('',
                    status=200,
                    mimetype='application/json')

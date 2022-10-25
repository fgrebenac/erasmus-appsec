import psycopg2 as psycopg2
from flask import Flask, request, Response
from res import *

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(host=host,
                            database=db_db,
                            user=db_user,
                            password=db_password)


def process_json(req):
    content_type = req.headers.get('Content-Type')
    print(content_type)
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


@app.route("/login", methods=['POST'])
def login():
    try:
        conn = get_conn()
        json_body = process_json(request)
        username = json_body['username']
        password = json_body['password']

        cur = conn.cursor()
        cur.execute('SELECT id FROM app_user '
                    'WHERE password = %s and username = %s',
                    (password, username))

        user = cur.fetchone()

        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return Response('{'
                        '   "error": "' + str(error) + '"'
                                                       '}',
                        status=400,
                        mimetype='application/json')

    if user is None or len(user) == 0:
        return Response('{'
                        '   "error": "User/Pass don\'t exist"'
                        '}',
                        status=400,
                        mimetype='application/json')

    return Response(str(user[0]),
                    status=200,
                    mimetype='application/json')


@app.route("/user", methods=['POST'])
def create_user():
    try:

        json_body = process_json(request)
        print(json_body)
        password = json_body['password']
        username = json_body['username']

        conn = get_conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO app_user (username, password)'
                    'values (%s, %s)',
                    (username, password))

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
def create_post(user_id):
    try:

        json_body = process_json(request)

        title = json_body['title']
        content = json_body['content']
        print(title + content)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO post (title, content, user_id)'
                    'values (%s, %s, %s)',
                    (title, content, user_id))

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
def get_posts(user_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT id, title, content FROM post p '
                    'WHERE user_id = %s',
                    user_id)

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
def get_post_by_id(user_id, post_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT id, title, content FROM post p '
                    'WHERE id = %s and user_id = %s',
                    (post_id, user_id))

        posts = cur.fetchmany()

        print(posts)

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
        return Response(prepare_post_resp(posts),
                        status=200,
                        mimetype='application/json')

@app.route("/user/<user_id>/post/<post_id>", methods=['DELETE'])
def delete_post_by_id(user_id, post_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM post '
                    'where id = %s and user_id = %s',
                    (post_id, user_id))

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

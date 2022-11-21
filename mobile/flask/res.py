import secrets

host = 'localhost'
db_db = 'mob_app'
db_user = 'postgres'
db_password = '123'
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
SECRET_KEY = secrets.token_hex()
tokens = {}

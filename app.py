from flask import Flask, request, render_template, redirect, make_response
from functools import wraps
import os
from psql.psql_funcs import Psql
from heroku_redis.redis_funcs import Redis
from security.jwt_check import JWT
from mail.smtp import Mail
from security.password_check import PassChek
from log.logger import Logger

if __name__ == '__main__':
    import set_env_values

psql = Psql(os.getenv('DATABASE_URL'))
redis = Redis(os.getenv('REDIS_URL'))
jwt = JWT(os.getenv('JWT_KEY'),
          os.getenv('JWT_ALGORITHM'))
mail = Mail(os.getenv('EMAIL_USER'),
            os.getenv('EMAIL_USER_PASSWORD'),
            os.getenv('SMTP'),
            os.getenv('SMTP_PORT'))
pchek = PassChek(os.getenv('HASH_METHOD'))

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/home')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def login_redirect():
    flask_resp = make_response(redirect('/login'))
    flask_resp.set_cookie('session_token', expires=0)
    return flask_resp


def generate_ttl(time_period: str) -> int:
    if time_period == '1 hour':
        return 3600
    if time_period == '1 day':
        return 86400
    if time_period == '3 days':
        return 259200
    if time_period == '1 week':
        return 604800


def jwt_check(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'session_token' in request.cookies:
            jwt_resp = jwt.check_token(request.cookies['session_token'])
            if jwt_resp:
                decoded_token = jwt.decode_token(request.cookies['session_token'])
                redis_resp = redis.check_token(decoded_token['decoded_token'],
                                               request.cookies['session_token'])
                if redis_resp:
                    return function(*args, **kwargs)
                else:
                    return login_redirect()
            else:
                return login_redirect()
        else:
            return login_redirect()

    return wrapper


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if 'password' in request.form and 'email' in request.form:
            psql_resp = psql.get_user_by_email(request.form['email'])
            if psql_resp['result']:
                user = psql_resp['user']
                pass_check_resp = pchek.check_password_hash(user.password, request.form['password'])
                if pass_check_resp:
                    flask_resp = make_response(redirect('/home'))
                    flask_resp.set_cookie('session_token',
                                          jwt.create_token(user.user_id, generate_ttl(request.form['time_period'])))
                    return flask_resp
                if not pass_check_resp:
                    return render_template('login.html', data='incorrect password')
            if not psql_resp['result']:
                return redirect('/register')
    if request.method == 'GET':
        if 'session_token' in request.cookies and jwt.check_token(request.cookies['session_token']):
            return redirect('/home')
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
@jwt_check
def logout():
    decoded_jwt = jwt.decode_token(request.cookies['session_token'])['decoded_token']
    redis.add_bad_token(decoded_jwt, request.cookies['session_token'])
    return login_redirect()


@app.route('/home', methods=['GET'])
@jwt_check
def home():
    decoded_jwt = jwt.decode_token(request.cookies['session_token'])
    return render_template('home.html', user_notes=psql.find_notes(decoded_jwt['decoded_token']['user_id']))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, redirect
from security.jwt_check import jwt_check
import os

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        print(request.args)
        return render_template('login.html')
    if request.method == 'POST':
        return request.form


if __name__ == '__main__':
    import set_env_values
    app.run(debug=True)

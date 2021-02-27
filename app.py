from flask import Flask

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return {
        "message": "Request method does not exist. "
    }, 404


@app.route('/')
def index():
    return 'lol', 300


@app.route('/status/<float:state>')
def status(state):
    if state == 'learn':
        return 'PPC BORING'
    if state == 'play':
        return 'VERY VERY GREAT SUPER NICE'
    else:
        return 'HZ'


if __name__ == '__main__':
    app.run(port=5123, debug=True)

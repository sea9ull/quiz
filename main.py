# import eventlet
# eventlet.monkey_patch()
from datetime import timedelta
from flask import Flask, redirect, url_for, \
        render_template, request, session
from flask_socketio import SocketIO, emit, \
        join_room, leave_room, close_room
from flask_httpauth import HTTPBasicAuth
import uuid
from lib.quiz import Quiz
from lib.user_local import User
# from lib.user import getAnswer, setAnswer, setUser, \
#         userCheck, totalScore, deleteAllAnswer

user = User()

HOST = "https://quiz-381905.uw.r.appspot.com"
# HOST = "http://127.0.0.1:8080"

SOCKET_USER_NS = "/quiz"
SOCKET_MASTER_NS = "/quiz_master"
QUIZ_ROOM = "quiz"
USERS = {
    "master": "2214"
}

# 非同期処理に使用するライブラリの指定
# `threading`, `eventlet`, `gevent`から選択可能
async_mode = None
app = Flask(__name__, template_folder='template', static_folder='resources')
app.config['SECRET_KEY'] = 'selria'

app.permanent_session_lifetime = timedelta(days=1)
# (minutes=5) -> 5分
# (days=5) -> 5日保存
auth = HTTPBasicAuth()

# socketio = SocketIO(app, async_mode=async_mode)
allowed_origins = "*"
# allowed_origins = "https://quiz-381905.uw.r.appspot.com"
socketio = SocketIO(app, cors_allowed_origins=allowed_origins)
thread = None
quiz = Quiz("resources/data/questions.json")

MESSAGES = {
    "user": {
        "START": {"title": "待機中", "message": "開始までしばらくお待ちください"},
        "SELECT": {"title": "問題の選択中", "message": "問題が選択されるまでしばらくお待ちください"},
        "QUESTION": {"title": "回答を送信しました", "message": "結果が出るまでしばらくお待ちください"},
        "FINISHED": {"title": "クイズは終了しました", "message": "ありがとうございました"}
    },
    "master": {
        "FINISHED": {"title": "クイズは終了しました", "message": "ありがとうございました"}
    }
}


@auth.get_password
def get_pw(user):
    if user in USERS:
        return USERS.get(user)
    return None


def getMasterState():
    state, data = quiz.getMasterState()
    obj = {}
    if state == "START":
        obj = {'type': 'START', 'data': '<div class="logo"><img src="/resources/blob/logo.svg"/></div>'}
    elif state == "FINISHED":
        obj = {'type': 'MESSAGE', 'data': MESSAGES["master"][state]}
    else:
        obj = {'type': state, 'data': data}
    return obj


def getUserState():
    state, data = quiz.getUserState()
    obj = {}
    hasAnswer, result = user.getAnswer(session.get('uid'), quiz.getId())
    if state == "QUESTION" and not hasAnswer:
        obj = {'type': state, 'data': data}
    elif state == "ANSWER":
        obj = {'type': state, 'data': {"result": result, "text": data}}
    else:
        obj = {'type': 'MESSAGE', 'data': MESSAGES["user"][state]}
    return obj


@app.route('/', methods=['GET'])
def home():
    if "uid" not in session:
        return redirect(url_for("signup"))
    return render_template('index.html')


@app.route('/master')
@auth.login_required
def master():
    return render_template('master.html')


@app.route('/admin')
@auth.login_required
def admin():
    return render_template('admin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/api/signup', methods=['POST'])
def api_signup():
    payload = request.get_json()
    user = str(payload["user"])
    uid = str(uuid.uuid1())
    session["uid"] = uid
    session["name"] = user
    user.setUser({"id": uid, "name": user})
    # return redirect(url_for("home"))
    return {"id": uid, "user": user}, 200


@app.route('/api/score', methods=['GET'])
def api_score():
    return {"score": user.totalScore()}, 200


@app.route('/api/resetUser', methods=['POST'])
def api_reset_user():
    user.deleteAllAnswer()
    return {"result": True}, 200


@app.route('/api/resetApp', methods=['POST'])
def api_reset_app():
    quiz.reset()
    emit('master_response', getMasterState(), namespace=SOCKET_MASTER_NS)
    emit('response', getUserState(), namespace=SOCKET_USER_NS, room=QUIZ_ROOM)
    return {"result": True}, 200


@socketio.on('connect', namespace=SOCKET_USER_NS)
def user_connect(data):
    join_room(QUIZ_ROOM)
    emit('response', getUserState(), namespace=SOCKET_USER_NS, room=QUIZ_ROOM)


@socketio.on('ready', namespace=SOCKET_USER_NS)
def ready(data):
    emit('response', getUserState(), namespace=SOCKET_USER_NS, room=QUIZ_ROOM)


@socketio.on('answer', namespace=SOCKET_USER_NS)
def answer(data):
    print(data)
    uid = session.get('uid')
    name = session.get('name')
    qid = quiz.getId()
    result = quiz.judgeAnswer(data["answer"])
    answer_text = ','.join(data["answer"])
    user.userCheck({"id": uid, "name": name})
    user.setAnswer({"id": uid, "qid": qid, "result": result, "answer": answer_text})
    emit('response', getUserState(), namespace=SOCKET_USER_NS, room=QUIZ_ROOM)


@socketio.on('connect', namespace=SOCKET_MASTER_NS)
def master_connect(data):
    emit('master_response', getMasterState(), namespace=SOCKET_MASTER_NS)


@socketio.on('master_ready', namespace=SOCKET_MASTER_NS)
def master_ready(data):
    emit('master_response', getMasterState(), namespace=SOCKET_MASTER_NS)


@socketio.on('master_next', namespace=SOCKET_MASTER_NS)
def master_next(data):
    quiz.next()
    emit('master_response', getMasterState(), namespace=SOCKET_MASTER_NS)
    emit('response', getUserState(), namespace=SOCKET_USER_NS, room=QUIZ_ROOM)


@socketio.on('master_select', namespace=SOCKET_MASTER_NS)
def master_select(data):
    quiz.select(data["id"])
    emit('master_response', getMasterState(), namespace=SOCKET_MASTER_NS)
    emit('response', getUserState(), namespace=SOCKET_USER_NS, room=QUIZ_ROOM)


if __name__ == '__main__':
    # socketio.run(app, host='127.0.0.1', port=8080, debug=True)
    socketio.run(app, host='127.0.0.1', port=443, debug=True)
    # app.run(host='127.0.0.1', port=8080, debug=True)

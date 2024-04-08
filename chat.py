from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

users = {}  # To track nicknames by session ID

@socketio.on('disconnect')
def handle_disconnect():
    nickname = users.pop(request.sid, None)
    if nickname:
        message = f'{nickname} disconnected'
        print(message)
        socketio.emit('my response', message)

@socketio.on('userNickname')
def handle_nickname(nickname):
    users[request.sid] = nickname  # Associate nickname with session ID
    message = f'{nickname} is on'
    print(message)
    socketio.emit('my response', message)

@socketio.on('my response')
def handle_chat_message(msg):
    nickname = users.get(request.sid, 'An anonymous user')
    message_sent = f'{nickname}: {msg}'
    print(f'Emitting message: {message_sent}') 
    socketio.emit('my response', message_sent)

if __name__ == '__main__':
    socketio.run(app, debug=True)
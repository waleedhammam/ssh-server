# imports
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import subprocess

# configuring flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# threading
async_mode = None
thread = None
socketio = SocketIO(app, async_mode=async_mode)

# background tasks
def background_thread():
    while True:
        socketio.sleep(10)
        socketio.emit('my response', namespace='/test')

# main app root
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

# sending commands to a shell
@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    p = subprocess.Popen(message['data'], stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    emit('my response',
         {'data': out, 'count': 0})

# app start
if __name__ == '__main__':
    socketio.run(app, debug=True)

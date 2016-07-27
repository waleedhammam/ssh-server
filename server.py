# imports
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, send
import subprocess


# configuring flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

@socketio.on('message', namespace='/BaseNamespace')
def handle_message(message):
    print('received message: ' + message)

# main app root
@app.route('/')
def index():
    socketio.emit('my response', namespace='/BaseNamespace')
    return render_template('index.html', async_mode=socketio.async_mode)

# sending commands to a shell
@socketio.on('my event', namespace='/BaseNamespace')
def test_message(message):
    p = subprocess.Popen(message['data'], stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()

    print out + " " + err
    emit('my response',
         {'data': out, 'count': 0})

# app start
if __name__ == '__main__':
    socketio.run(app, debug=True)

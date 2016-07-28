# imports
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, send
import subprocess


# configuring flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

# main app root
@app.route('/')
def index():
    socketio.emit('my response')
    return render_template('index.html', async_mode=socketio.async_mode)

# sending commands to a shell
@socketio.on('my event')
def test_message(message):
    p = subprocess.Popen(message['data'], stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    print out + " " + err
    emit('my response', [out, err])

# app start
if __name__ == '__main__':
    socketio.run(app, debug=True)

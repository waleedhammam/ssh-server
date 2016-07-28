from socketIO_client import SocketIO

# Send commands
data = raw_input('$: ')
socketIO = SocketIO('http://127.0.0.1', 5000)
socketIO.emit('my event', {'data': 'I\'m connected!'});
socketIO.emit('my event', {'data': data});
print('command sent! waiting for reply ..')
socketIO.wait(seconds=1)


# receive results
def on_response(*args):
    print('Received Data\n', args)


# Listen only once
socketIO.on("my response", on_response)
socketIO.wait(seconds=1)

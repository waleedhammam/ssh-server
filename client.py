from socketIO_client import SocketIO

# receive results
def on_response(*args):
    x = list(args)
    print 'Received Data:\n', args

# Send commands
data = raw_input('$: ')
socketIO = SocketIO('http://127.0.0.1', 5000)
socketIO.emit('my event', {'data': data}, on_response);
print('command sent! waiting for reply ..')

# Listen to sockets
socketIO.on("my response", on_response)
socketIO.wait_for_callbacks(seconds=1)

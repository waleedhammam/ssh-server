from __future__ import print_function
from socketIO_client import SocketIO, BaseNamespace
#for recieving from the server
def on_response(*args):
    print(args[0].get('data'))

socketIO = SocketIO('localhost', 5000, namespace="/test")
msg = ""
while msg != "exit":
    msg = raw_input(">>>")
    socketIO.emit('my event', {'data': msg }, lambda x: None)

    #import pudb; pu.db

    # Listen
    socketIO.on('my response', on_response)
    socketIO.wait_for_callbacks(seconds=1)

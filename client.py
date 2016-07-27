from socketIO_client import SocketIO, BaseNamespace

class Namespace(BaseNamespace):

    def on_aaa_response(self, *args):
        print('on_aaa_response', args)
        self.emit('ls')
        print('ls send!')

socketIO = SocketIO('localhost', 5000, Namespace)
socketIO.emit('ls')
print('ls sent')
socketIO.wait(seconds=1)

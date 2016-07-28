from __future__ import print_function
import websocket
user_in = raw_input(">>>")
while user_in != "exit" :
    user_in = raw_input(">>>")
    if user_in :
        websocket.enableTrace(True)
        ws = websocket.create_connection("ws://localhost:5000/")
        # ws.run_forever(sslopt={"check_hostname": False})
        print("Sending 'Hello, World'...")
        ws.send(user_in)
        print("Sent")
        print("Receiving...")
        result = ws.recv()
        print("Received '%s'" % result)
ws.close()

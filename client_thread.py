import socket
import threading

host = '127.0.0.1'
port = 54321
messages = ['Message 1', 'Message 2']

class ServerThread(threading.Thread):
    def __init__(self, conn, message):
        threading.Thread.__init__(self)
        self.conn = conn
        self.message = message
    def run(self):
        msgx = str('Message from ' + threading.current_thread().name + ': ' + self.message)
        print('[+] Sending message to server')
        self.conn.send(str.encode(msgx))
        while True:
            msg = self.conn.recv(1024)
            print('[M] Message received from the server', msg.decode())
            if not msg or len(msg) == len(msgx):
                print('[-] Closing connection to server')
                break
        self.conn.close()

# msgx = b'Hello, im client'
# s.send(msgx)
# while True:
#     msg = s.recv(1024)
#     print('Message received from the server', msg.decode())
#     if len(msg) == len(msgx):
#         break
for message in messages:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    thread = ServerThread(s, message)
    thread.start()
    thread.join()
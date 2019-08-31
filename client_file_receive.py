import socket
import threading
import time

host = '127.0.0.1'
port = 54321
receivefile = 'Receive' + str(int(time.time())) + '.csv'

class ServerFileReceive(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        print('[+] Connected to host')
        self.conn = conn
    def run(self):
        msgx = 'Message from ' + threading.current_thread().name
        self.conn.send(msgx.encode())
        while True:
            f = open(receivefile, 'wb')
            msg = self.conn.recv(1024)
            if not msg:
                self.conn.close()
                f.close()
                print('[-] Connection to host teminated')
                break
            f.write(msg)
            print('[M] Message from the server:', repr(msg))

s = socket.socket()
s.connect((host, port))
thread = ServerFileReceive(s)
thread.start()
thread.join()

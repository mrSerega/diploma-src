import socket
from threading import Thread
import time

class serv_thread(Thread):

    callBack = lambda : 2

    def __init__(self, callBack):
        Thread.__init__(self)
        self.callBack = callBack

    def run(self):
        while True:
            time.sleep(1)
            self.callBack()

class serv:

    pull = []
    threads = []

    def __init__(self):
        pass

    def set_ports_pull(self, pull):
        self.pull = pull

    def start_serv(self):
        for port in self.pull:
            print(port)
            self.threads.append(serv_thread(lambda : self.new_server_conn(port)))

        for thread in self.threads:
            thread.start()

    def new_server_conn(self, port):
        sock = socket.socket()
        print(port)
        sock.bind(('', port))
        sock.listen(1)
        conn, addr = sock.accept()
        self.do_connection(conn)

    def do_connection(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print (data)
            self.send_task(conn)
            data = conn.recv(1024)
            print (data)
        conn.close()


    def send_task(self, conn):
        conn.send('task'.encode())

class client:

    def new_client_conn(self, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        sock.send('new request'.encode())

        data = sock.recv(1024)
        print(data)
        self.send_answer(sock)
        # sock.close()


    def send_answer(self, sock):
        sock.send('answer'.encode())

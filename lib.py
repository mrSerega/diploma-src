import socket
import threading
import time
import task_lib_primal
import sys

data = threading.local()

class serv_thread(threading.Thread):

    isStop = False

    def __init__(self, port):
        self.port = port
        threading.Thread.__init__(self)


    def run(self):
        data.x = self.name
        data.port = self.port
        while True:
            if serv.varbose: print ('thread: {} port: {}'.format(data.x, data.port))
            code = serv.new_server_conn(data.port)
            if code == 'NO_TASK':
                print ('stop: ', data.x)
                serv_thread.isStop = True
                break

class watcher(threading.Thread):
    def __init__(self, server):
        self.server = server
        threading.Thread.__init__(self)

    def run(self):
        while (True):
            if serv_thread.isStop:
                print ('stopping...')
                self.server.send_trash()
                break
        print (self.server.tasker.answers)

class serv:

    varbose = False

    isStop = False
    tasker  = task_lib_primal.abstract_tasker()

    pull = []
    threads = []

    def __init__(self):
        pass

    def set_ports_pull(self, pull):
        self.pull = pull

    def start_serv(self):
        for port in self.pull:
            self.threads.append(serv_thread(port))
            

        for thread in self.threads:    
            thread.start()

        watch = watcher(self)
        watch.run()

    def send_trash(self):
        clnt = client()
        for sock in self.pull:
            try:
                clnt.new_client_conn('127.0.0.1', sock)
            except Exception:
                print ('closed ', sock)

    @staticmethod
    def new_server_conn(port):
        sock = socket.socket()
        if serv.varbose: print(port)
        try:
            sock.bind(('', port))
        except Exception:
            print ('cant create connection on ', port)
            return
        if serv.varbose: print ('created connection on {}'.format(port))
        sock.listen(1)
        conn, addr = sock.accept()
        code = serv.do_connection(conn)
        if code == 'NO_TASK':
            return 'NO_TASK'

    @staticmethod
    def do_connection(conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            if serv.varbose: print (data)
            code = serv.send_task(conn)
            if code == 'NO_TASK':
                return 'NO_TASK'
            data = conn.recv(1024)
            if serv.varbose: print (data)
            serv.tasker.add_answer(data)
            sys.stdout.write('progress: {}\r'.format(serv.tasker.status()))
        conn.close()


    @staticmethod
    def send_task(conn):
        task = serv.tasker.get_task()
        if serv.varbose:  print ('task: ', task)
        if task == 'NO_TASK':
            conn.send('NO_TASK'.encode())
            return 'NO_TASK'
        conn.send(task.encode())

class client:

    solver = lambda x: x

    def new_client_conn(self, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        sock.send('new request'.encode())

        data = sock.recv(1024)
        if serv.varbose: print(data)
        code = self.send_answer(sock, data)
        if code == 'NO_TASK':
            return 'NO_TASK'
        # sock.close()


    def send_answer(self, sock, data):
        if data == 'NO_TASK':
            return 'NO_TASK'
        ans = self.solver(data)
        if serv.varbose: print (ans)
        sock.send(ans.encode())

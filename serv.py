import lib
import task_lib_primal

server = lib.serv()
server.set_ports_pull([1340, 1341, 1342])
# server.set_ports_pull([1343, 1338, 1349])
lib.serv.tasker = task_lib_primal.tsker([el for el in range(1000)])
server.start_serv()
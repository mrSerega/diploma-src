import lib
import task_lib_primal
import sys

port = int(sys.argv[1]) or 1337

clnt = lib.client()
clnt.solver = task_lib_primal.solve
print ('client will create connection on ', port)
except_count = 0
while True:
    try:
        code = clnt.new_client_conn('127.0.0.1', port)
        if code == 'NO_TASK':
            print ('NO_TASK')
            break
        except_count = 0
    except Exception:
        except_count +=1
    if except_count > 1000:
        print ('stoping client')
        break
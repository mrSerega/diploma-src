import lib

serv = lib.serv()
serv.set_ports_pull([1337,1338])
serv.start_serv()
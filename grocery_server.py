import socket
from _thread import *
import threading

global flag
global true
global false
global done
global print_lock

print_lock = threading.Lock()
true = bytes("true", 'utf-8')
false = bytes("false", 'utf-8')
done = bytes("done", 'utf-8')


def con():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9997)
    print('Starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    sock.listen(5)


def client_con():
    while True:
        c, addr = sock.accept()
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(recieve, (c,))



d = {'Tomato':20,'Potato':10,'Onion':40,'Carrot':10,'Apple':45}
l=[]
def recieve(connection):
    
    amount=0
    while True:
        data = connection.recv(1024)
        s = str(data, 'utf-8')
        f= open('grocery_list.txt','r') 
        item=f.readlines()
        flag = 0
        for line in item:
            for word in line.split():
                # flag = -1
                #for word in line.split():
                if s.lower() == word:
                    flag =1
                    connection.sendall(true)
                                        
                else:
                    continue
        if(flag != 1):
            connection.sendall(false)
            print_lock.release()          
        data = connection.recv(1024)
        cand = str(data, 'utf-8')
        uppercand = cand.upper()
            if (uppercand == "YES" or uppercand =='Y'):
                  connection.sendall(true)
            else:
                  connection.sendall(false)
                  r = open("prices.txt", 'w')
                  for i in l:
                        r.write(str(i))
                        r.write("\n")
                  r.close()
                  break


            data = connection.recv(1024)
            final = str(data, 'utf-8')
            if final == "exit":
                  print_lock.release()
                  break

def close(s, data):
    print("Closing current connections")
    for i in range(2):
        connection[i].sendall(data)
        connection[i].close()
    print(s)

con()
client_con()
sock.close()

import socket
import time
import numpy as np
from sign.lyu_gen import Sign
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(("127.0.0.1",8083))
server.listen(100)
print('[+]  server open')
c_server = {}
server.setblocking(0)
online_dict={}
SIGN_KEY=np.load('ssig.npy')
def current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
def msg_process(msg,a):
    command=msg[:3]
    username=msg[3:].decode('utf-8')
    if command==b"add":
        if username in online_dict:
            a.sendall(b'add'+str(online_dict[username]).encode('utf-8'))
        else:
            a.sendall(b'off')
    elif command==b"pub":
        pub_key = np.load(username + "pub.npy")
        z, c=Sign(str(pub_key), SIGN_KEY)
        a.sendall(c.tostring()+z.tostring()+ pub_key.tostring())
    elif command==b"ver":
        ver_key = np.load(username + "ver.npy")
        z,c=Sign(str(ver_key), SIGN_KEY)#168019
        a.sendall(c.tostring()+z.tostring()+ ver_key.tostring())
    elif command==b'on_':
        online_dict[username] = c_server[a]
        print(username,' on ', c_server[a])
        c_server[a]=username
while True:
    try:
        client,c_addr = server.accept()
    except BlockingIOError:
        if not c_server:
            continue
        pass
    else:
        client.setblocking(0)
        c_server[client] = c_addr
        print('Connect from',c_addr)
    for a in list(c_server.keys()):
        try:
            msg = a.recv(10240)
        except BlockingIOError:
            continue
        except ConnectionResetError:
            print('[%s] closed'%(str(c_server[a])))
            a.close()
            if type(c_server[a])!=tuple:
                del online_dict[c_server[a]]
            del c_server[a]
            continue
        else:
            if msg==b'':
                continue
            print("来自%s的消息:"%(str(c_server[a])),msg)
            msg_process(msg,a)


import socket
import time
import numpy as np
from sign.lyu_gen import Verify

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #设置端口复用
#AF_INET: IPV4
#AF_INET6: IPV6
#SOCK_STREAM: TCP
#SOCK_DGRAM: UDP
server.bind(("127.0.0.1",8083))
#服务器绑定端口 8083
server.listen(100)#服务器同时监听5个 最大链接数 5

print('[+]  server open')

c_server = {}                      #定义一个全局字典  socket:address/name
server.setblocking(0)            #是否阻塞（默认True），如果设置False，那么accept和recv时一旦无数据，则报错。

online_dict={}#"username":address
swiftnumber_dict={}

def current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def msg_process(msg,a):
    command=msg[:3]
    username=msg[3:]
    if command==b"add":
        if username in online_dict:
            a.send(b'add'+str(online_dict[username]).encode('utf-8'))
        else:
            a.send(b'off')
    elif command==b"pub":
        pub_key = np.load(username + "pub.npy")
        a.send(b'pub' + pub_key.tostring())
    elif command==b"ver":
        ver_key = np.load(username + "ver.npy")
        a.send(b'pub' + ver_key.tostring())
    elif command==b'on_':
        c = np.fromstring(username[:80], np.int8)
        z = np.fromstring(username[80:4176], np.int32)
        swift_number=int(username[4176:4184].decode('utf-8'))
        name = username[4184:].decode('utf-8')
        flag=True

        try:
            Ver_key=np.load('register/'+name+"ver.npy")
        except:
            flag&=False
        else:
            flag &= Verify(c, z, str(swift_number) + name, Ver_key)

        try:
            if swift_number <= swiftnumber_dict[name]:
                flag &= False
        except:
            pass

        if flag==True:
            swiftnumber_dict[name] = swift_number
            online_dict[name] = a.getsockname()
            c_server[a]=name
            print('from', c_addr, name)
        else:
            a.close()
            del c_server[a]

while True:
    try:
        client,c_addr = server.accept()
    except BlockingIOError:
        if not c_server:            #如果字典为空
            continue            #重新接收套接字
        pass
    else:
        client.setblocking(0)#设置套接字属性为非阻塞
        c_server[client] = c_addr  # 以字典形式存储新链接的套接字
        print('[+] from',c_addr)

    for a in list(c_server.keys()):        #这里将字典的keys取出来
        try:
            msg = a.recv(10240)            #非阻塞接受消息，但是如果没有收到信息，就会报错,我们就接着下一个
        except BlockingIOError:
            continue
        except ConnectionResetError:
            print('[%s] closed'%(str(c_server[a])))
            a.close()
            if type(c_server[a])==tuple:
                del online_dict[c_server[a]]
            del c_server[a]#断开的时候删除套接字了
            continue
        else:
            print("来自%s的消息"%(str(c_server[a])))
            print(len(msg))
            msg_process(msg,a)

server.close()
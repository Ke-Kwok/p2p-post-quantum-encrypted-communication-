# import time
# from encrypt.ntru_generator import generate
# import sys
# from sign.lyu_gen import KeyGen
# import numpy as np
# time1=time.time()
# for i in range(100):
# priv_key,pub_key=KeyGen()
#
# time2=time.time()
# print(time2-time1)
# pub_key1=np.array(pub_key).astype(np.int8)[::-1]
# s=pub_key1.tostring()
# # s=np.zeros(10,dtype=np.int8)
# print(sys.getsizeof(s))#96   167*int8
# s2=str(pub_key).encode('utf-8')
# print(sys.getsizeof(s2))
# f=priv_key['f']
# f_p=priv_key['f_p']

# pub_key1=np.array(f).astype(np.int8)[::-1]
# s=pub_key1.tostring()
# # s=np.zeros(10,dtype=np.int8)
# print(sys.getsizeof(s))#96   167*int8
# s2=str(f).encode('utf-8')
# print(sys.getsizeof(s2))

# pub_key1=np.array(f_p).astype(np.int8)[::-1]
# s=pub_key1.tostring()
# # s=np.zeros(10,dtype=np.int8)
# print(sys.getsizeof(s))#96   167*int8
# s2=str(f_p).encode('utf-8')
# print(sys.getsizeof(s2))
# # print(f.__sizeof__())
# # print(f_p.__sizeof__())
# # print(pub_key.__sizeof__())
# #print(sys.getsizeof(priv_key))

# import socket
# #单进程服务器 实现多客户端访问 IO复用
# #吧所有的客户端套接字 放在一个列表里面，一次又一次的便利过滤
# #这就是apache： select模型 6
#
# server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #设置端口复用
# #AF_INET: IPV4
# #AF_INET6: IPV6
# #SOCK_STREAM: TCP
# #SOCK_DGRAM: UDP
# # Host = ''
# # port = 23333
# server.bind(("127.0.0.1",8083))
# #服务器绑定端口 8080
# server.listen(5)
# #服务器同时监听5个 最大链接数 5
#
# print('[+]  server open')
#
# c_server = {}
# #定义一个全局字典
# server.setblocking(0)
# #设置服务器recv接受信息和send发送信息为非阻塞状态（默认为阻塞状态）
# #是否阻塞（默认True），如果设置False，那么accept和recv时一旦无数据，则报错。
# while True:
#     try:
#         try:
#
#             client,c_addr = server.accept()
#
#         except BlockingIOError:
#             #无法立即完成一个非阻止性套接字操作。
#             if not c_server:
#                 #如果字典为空
#                 continue
#                 #重新接收套接字
#             pass
#         else:
#             client.setblocking(0)#设置套接字属性为非阻塞
#             #是否阻塞（默认True），如果设置False，那么accept和recv时一旦无数据，则报错。
#             #[WinError 10035] 无法立即完成一个非阻止性套接字操作。
#             c_server[client] = c_addr#以字典形式存储新链接的套接字
#             print('[+] from',c_addr)
#         for a in list(c_server.keys()):
#             #这里将字典的keys取出来 在列表化,在没有信息的时候删除套接字了
#             try:
#                 msg = a.recv(1024).decode('utf-8')
#                 #非阻塞接受消息，但是如果客户端不马上发送，就会报错，所以设置一个延迟接收
#             except BlockingIOError as e:
#                 continue
#
#             if not msg:
#                 print('[%s] closed'%(c_server[a][0]))
#                 a.close()
#                 del c_server[a]
#                 continue
#             print("来自%s的消息： %s"%(c_server[a][0],msg))
#             a.send(msg.encode('utf-8'))
#             #发送重复的消息
#     except KeyboardInterrupt:
#         break
#
# server.close()
# import numpy as np
#
# apub=np.load("register/apub.npz")
# pub_key=apub['pub_key']#.tostring()
# ver_key=apub['ver_key']#.tostring()
# # str(list(ver_key)).encode()
# # print(ver_key.__sizeof__())
# # print(pub_key.__sizeof__())
# np.save("apub.npy",pub_key)
# np.save("aver.npy",ver_key)

# s={'dasda':2,'dada':1}
# del s['dada']
# print(s['dada'])
# s1=(1,2)
# print(type(s1)==tuple)
# import numpy as np
# s=np.array([1,2])
# m=s.tostring()
# print(m.__sizeof__())
# k=str(m)
# print(k.__sizeof__())
# print(m)
# print(str(s))
# l=str(s)
# print(l.__sizeof__())
# print(m.decode('utf-8'))
#
# ss=np.load('register/spriv.npz')
# np.save('ssig.npy',ss['sign_key'])
import numpy as np
#
# A=np.array([3,4])
# B=np.array([1,2])
# np.save( "priv.npy",{'a':A,'b':B})
# s=np.load('priv.npy')
# #m=dict(s)
# print(type(s.item()))
#np.savez_compressed('dasda',m)
from sign.lyu_gen import Verify,Sign
SIGN_KEY=np.load('ssig.npy')#['sign_key']
#np.save("ssig.npy",SIGN_KEY)
#Ver_key=np.load('sver.npy')
msg1 = np.load( "bver.npy")

z, c= Sign(str(msg1), SIGN_KEY)
# # m=c.tostring() + z.tostring() + msg1.tostring()
# # c = np.fromstring(m[:80], dtype=np.int8)
# # z = np.fromstring(m[80:4176], dtype=np.int32)
# # pub = np.fromstring(m[4176:], dtype=np.int8)
#print(Verify(c,z,str(msg1),Ver_key))

# z, c = Sign(str(msg1), SIGN_KEY)

msg = b'on_'+c.tostring() + z.tostring() + msg1.tostring()#.encode('utf-8')

print(len(msg))

print(len(str(msg1)))
print(len(str(msg1.tostring())))

command = msg[:3]
username = msg[3:]
c = np.fromstring(username[:80], np.int8)
z = np.fromstring(username[80:4176], np.int32)
msg1=np.fromstring(username[4176:], np.int32).reshape((512,80))
# swift_number = int(username[4176:4184].decode('utf-8'))
# name = username[4184:].decode('utf-8')
#Ver_key = np.load("sver.npy")
print(Verify(c, z, str(msg1), Ver_key))

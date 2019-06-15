import tkinter as tk
from tkinter import messagebox,scrolledtext,END,DISABLED,NORMAL
import win32ui
import time
import socket
import numpy as np
from NTRU_cryptosystem.encrypt import encrypt
from NTRU_cryptosystem.decrypt import decrypt
from Lyubashevsky_signature.lyu12vK import Sign,Verify
import threading
server_address = ("127.0.0.1", 8083)
try:
    pub_dict=np.load('apub.npy').item()
except:
    pub_dict={}
try:
    ver_dict=np.load('aver.npy').item()
except:
    ver_dict={}
try:
    send_swift_dict=np.load('a_sendswift.npy').item()
except:
    send_swift_dict={}
try:
    recv_swift_dict = np.load('a_recvswift.npy').item()
except:
    recv_swift_dict = {}
send_dict={}
recv_dict={}
ip_dict={}
s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_server.connect(server_address)
my_add=s_server.getsockname()
my_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(my_add)
my_socket.listen(100)
my_socket.setblocking(0)
Ver_key=np.load("sver.npy")
def current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '
class LoginPage():
    def __init__(self,master=None):
        self.root=master
        self.root.geometry('450x300')
        self.username=tk.StringVar()
        self.createPage()
    def createPage(self):
        self.page=tk.Frame(self.root)
        self.page.pack(fill='both',expand=1)
        tk.Label(self.page, text='用户名:').place(x=50, y=180)
        tk.Entry(self.page, textvariable=self.username).place(x=150, y=180)
        tk.Button(self.page, text='登陆', command=self.loginCheck).place(x=170, y=230)
    def loginCheck(self):
        global priv,SIGN_KEY,PRIV_KEY_f, PRIV_KEY_f_p,my_name
        my_name=self.username.get()
        try:
            priv=np.load(my_name+"priv.npz")
        except:
            tk.messagebox.showerror(title='错误', message='用户名错误！')
        else:
            PRIV_KEY_f, PRIV_KEY_f_p,SIGN_KEY=priv['priv_key_f'],priv['priv_key_f_p'],priv['sign_key']
            on_msg =b'on_'+ my_name.encode('utf-8')
            s_server.sendall(on_msg)
            self.page.destroy()
            MainPage(self.root)
class MainPage():
    def __init__(self,master=None):
        self.root=master
        self.root.geometry('450x300')
        self.object_name=tk.StringVar()
        self.hide_message=tk.StringVar()
        self.hide_message = ''
        self.button_text=tk.StringVar()
        self.button_text="暂停显示"
        self.createPage()
    def createPage(self):
        self.page=tk.Frame(self.root)
        self.page.pack(fill='both',expand=1)
        tk.Label(self.page, text=my_name+'的数据显示区 ').place(x=0, y=0)
        self.display=tk.scrolledtext.ScrolledText(self.page,width=50,height=9,state=DISABLED)
        self.display.place(x=0, y=20)
        tk.Button(self.page, text='保存显示', command=self.save).place(x=380, y=20)
        tk.Button(self.page, text='清空显示', command=self.clear).place(x=380, y=60)
        stop_start_button=tk.Button(self.page, text=self.button_text,fg='red', command= lambda:self.stop_start(stop_start_button))
        stop_start_button.place(x=380, y=100)
        tk.Label(self.page, text='目标用户名 ').place(x=0, y=150)
        tk.Entry(self.page, textvariable=self.object_name,width=40).place(x=70, y=150)
        send_msg=tk.scrolledtext.ScrolledText(self.page,width=50,height=8,wrap=tk.WORD)
        send_msg.place(x=0, y=180)
        tk.Button(self.page, text='发送消息', command= lambda:self.send(send_msg)).place(x=380, y=180)
        threading.Thread(target=self.recv_msg).start()
    def save(self):
        dlg = win32ui.CreateFileDialog(0)
        dlg.SetOFNInitialDir("C:")
        flag = dlg.DoModal()
        if 1 == flag:
            file_path=dlg.GetPathName()+'.txt'
            with open(file_path,'a') as f:
                f.write(self.display.get(1.0,END))
    def clear(self):
        self.display.config(state=NORMAL)
        self.display.delete(1.0,END)
        self.display.config(state=DISABLED)
    def stop_start(self,stop_start_button):
        if self.button_text=="暂停显示":
            self.button_text ="重启显示"
            stop_start_button.config(fg='green')
        else:
            self.button_text = "暂停显示"
            self.display.config(state=NORMAL)
            self.display.insert(END, self.hide_message)
            self.display.config(state=DISABLED)
            self.hide_message = ''
            stop_start_button.config(fg='red')
        stop_start_button.config(text=  self.button_text)
    def send(self,send_msg):
        my_msg=send_msg.get(1.0,END)
        if my_msg !='\n':
            if self.object_name.get() =='':
                tk.messagebox.showerror(title='错误', message='目标用户名不能为空！')
            else:
                if self.send_message(self.object_name.get(),my_msg):
                    display_msg = current_time() + ">" + self.object_name.get() + ":" + my_msg
                    if self.button_text == "暂停显示":
                        self.display.config(state=NORMAL)
                        self.display.insert(END, display_msg)
                        self.display.config(state=DISABLED)
                    else:
                        self.hide_message += display_msg
                    send_msg.delete(1.0, END)
                else:
                    tk.messagebox.showerror(title='错误', message='目标用户不在线')
    def send_message(self, object_name,my_msg):
        while(True):
            if object_name not in ip_dict:
                s_server.sendall(b"add" + object_name.encode("utf-8"))
                recv = s_server.recv(1024)
                if recv[:3] == b'add':
                    ip_dict[object_name] = eval(recv[3:].decode("utf-8"))
                elif recv[:3] == b'off':
                    return 0
            elif object_name not in pub_dict:
                s_server.sendall(b"pub" + object_name.encode("utf-8"))
                recv = s_server.recv(8192)
                c=np.fromstring(recv[:80], dtype=np.int8)
                z=np.fromstring(recv[80:4176],dtype=np.int32)
                pub=np.fromstring(recv[4176:], dtype=np.int8)
                if Verify(c,z,str(pub),Ver_key):
                    pub_dict[object_name] = pub
            elif object_name not in send_dict:
                s_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s_object.connect(ip_dict[object_name])
                except ConnectionRefusedError:
                    s_object.close()
                    continue
                send_dict[object_name] = s_object
            else:
                if object_name not in send_swift_dict:
                    send_swift_dict[object_name] = 10000000
                input_arr = np.trim_zeros(np.unpackbits(np.frombuffer(my_msg.encode('utf-8'), dtype=np.uint8)), 'b')
                enc_mes = encrypt(pub_dict[object_name], input_arr)
                z, c = Sign(str(send_swift_dict[object_name]) + my_msg, SIGN_KEY)
                sign_enc_msg = c.tostring() + z.tostring() + (
                            str(send_swift_dict[object_name]) + str(len(my_name)) + my_name).encode(
                    'utf-8') + enc_mes.tostring()+b'end'
                try:
                    send_dict[object_name].sendall(sign_enc_msg)
                    send_swift_dict[object_name]+=1
                    return 1
                except ConnectionResetError:
                    print('[%s] is offline' % object_name)
                    del send_dict[object_name]
                    del ip_dict[object_name]
                    return 0
    def recv_msg(self):
        while(True):
            try:
                client, c_addr = my_socket.accept()
            except BlockingIOError:
                pass
            else:
                client.setblocking(0)
                recv_dict[client] = c_addr
                print('Connect from', c_addr)
            for a in list(recv_dict.keys()):
                try:
                    msg=b''
                    while True:
                        m = a.recv(8192)
                        msg+=m
                        if b'end' in msg:
                            break
                except BlockingIOError:
                    continue
                except ConnectionResetError:
                    print('[%s] closed' % (str(recv_dict[a])))
                    a.close()
                    del recv_dict[a]
                    continue
                else:
                    c = np.fromstring(msg[:80], np.int8)
                    z = np.fromstring(msg[80:4176], np.int32)
                    swift_number = int(msg[4176:4184].decode('utf-8'))
                    name_len=int(msg[4184:4185].decode('utf-8'))
                    name = msg[4185:4185+name_len].decode('utf-8')
                    enc_mes=msg[4185+name_len:-3]
                    if type(recv_dict[a])==tuple:
                        recv_dict[a]=name
                    print("来自%s的消息" % (str(recv_dict[a])))
                    if name in recv_swift_dict:
                        if swift_number<=recv_swift_dict[name]:
                            continue
                    recv_swift_dict[name] = swift_number
                    recv_arr = np.fromstring(enc_mes, dtype=np.int8)
                    output = decrypt(PRIV_KEY_f, PRIV_KEY_f_p, recv_arr)
                    out = np.packbits(np.array(list(map(int, output))))
                    dec_msg = ''
                    for i_ in out:
                        dec_msg += str(chr(i_))  # 码为ord
                    if name not in ver_dict:
                        while(True):
                            s_server.sendall(b"ver" + name.encode("utf-8"))
                            recv = s_server.recv(204800)
                            c1 = np.fromstring(recv[:80], dtype=np.int8)
                            z1 = np.fromstring(recv[80:4176], dtype=np.int32)
                            ver = np.fromstring(recv[4176:], dtype=np.int32).reshape((512,80))
                            if Verify(c1, z1, str(ver), Ver_key):
                                ver_dict[name] = ver
                                break
                            print("签名公钥验证失败")
                    if Verify(c,z,str(swift_number)+dec_msg,ver_dict[name]):
                        display_msg = current_time() +name+  ">" + ":" + dec_msg
                        if self.button_text == "暂停显示":
                            self.display.config(state=NORMAL)
                            self.display.insert(END, display_msg)
                            self.display.config(state=DISABLED)
                        else:
                            self.hide_message += display_msg
                    else:
                        print("验证失败")
root=tk.Tk()
root.title('Post-quantum P2P communication')
LoginPage(root)
root.mainloop()
s_server.close()
np.save('apub.npy',pub_dict)
np.save('aver.npy',ver_dict)
np.save('a_sendswift.npy',send_swift_dict)
np.save('a_recvswift.npy',recv_swift_dict)
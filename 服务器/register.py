from sign.lyu_gen import KeyGen
from encrypt.ntru_generator import generate
import numpy as np
A=np.load("A.npy")
priv_key_f,priv_key_f_p,pub_key=generate()
sign_key, ver_key=KeyGen()
while(True):
    name = input("Enter User name (length less than 10):")
    if len(name)>9:
        continue
    try:
        np.load(name+"pub.npy")
    except:
        np.savez_compressed(name+"priv",A=A,priv_key_f=priv_key_f,priv_key_f_p=priv_key_f_p,sign_key=sign_key)
        np.save(name+"pub.npy",pub_key)
        np.save(name+"ver.npy",ver_key)
        break
    print(name+" has been registered! Enter another name.")


import numpy as np
from  sign import util
import random
n, m, k, d, q, std = 512, 1024, 80, 1, pow(2, 24), 30720
def KeyGen():
    A=np.load("A.npy")
    S = util.crypt_secure_matrix(-d, d, m, k)
    T = util.matrix_to_Zq(np.matmul(A, S), q)
    sign_key=S.astype(np.int8)
    ver_key=T.astype(np.int32)
    return sign_key,ver_key
def Verify(c,z,msg,ver_key):
    A=np.load("A.npy")
    T=ver_key
    norm_bound = 4 * std*std * m
    vec = util.vector_to_Zq(np.matmul(A,z) - np.matmul(T,c), q)
    hashedList = util.hash_to_baseb(vec, msg, 3, k)
    if z.dot(z.astype(np.int64)) <= norm_bound and np.array_equal(c, hashedList):
        return True
    else:
        return False
def Sign(msg, sign_key):
    A=np.load("A.npy")
    S=sign_key
    while(True):
        y =util.DiscreteGuassianDistribution(0,std,m)
        vec=util.vector_to_Zq(np.matmul(A,y), q)
        c = util.hash_to_baseb(vec, msg, 3, k)
        Sc = np.matmul(S,c)
        z = Sc + y
        pxe = float(-2*z.dot(Sc) + Sc.dot(Sc))
        val = np.exp(pxe / (2*std**2)) / 2.72
        if(random.random() < val):
            break
    return z, c.astype(np.int8)

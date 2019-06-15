import numpy as np
import hashlib as hl
def RouletteWheelSelection(c):
    s=np.random.rand()
    for i in range(len(c)):
        if c[i]>s:
            if np.random.rand()>0.5:
                return i
            else:
                return -i
def DiscreteGuassianDistribution(v,std,size):
    c = [0.5]
    len=np.int(12*std)+1
    for i in range(1,len):
        c.append(np.exp(-i*i/ (2 * std*std)))
    c=c/sum(c)
    for i in range(1,len):
        c[i]=c[i]+c[i-1]
    res=np.zeros(size,dtype=np.int)
    for i in range(size):
        res[i]=RouletteWheelSelection(c)
    return res+v
def to_integer_ring(ele, q):
    if ele % q <= (q-1)/2:
        return (ele % q)
    else:
        return (ele % q) - q
def matrix_to_Zq(M, q):
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            M[i][j] = to_integer_ring(M[i][j], q)
    return M
def vector_to_Zq(v, q):
    for i in range(len(v)):
        v[i] = to_integer_ring(v[i],q)
    return v
def hash_to_baseb(matrix, message, b, k):
    hexval = hl.sha512((np.array_str(matrix) + message).encode('utf-8')).hexdigest()
    return np.array(list(map(int, list(b2b(hexval, 16, b)[:k]))))-1
base_symbols='0123456789abcdefghijklmnopqrstuvwxyz'
def v2r(n, b):
    digits = ''
    while n > 0:
        digits = base_symbols[n % b] + digits
        n  = n // b
    return digits
def r2v(digits, b):
    n = 0
    for d in digits:
        n = b * n + base_symbols[:b].index(d)
    return n
def b2b(digits, b1, b2):
    return v2r(r2v(digits, b1), b2)


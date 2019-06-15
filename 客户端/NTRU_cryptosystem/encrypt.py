from NTRU_cryptosystem.ntrucipher import NtruCipher
from NTRU_cryptosystem.mathutils import random_poly
from sympy.abc import x
from sympy import ZZ, Poly
import numpy as np
import math
def padding_encode(input_arr, block_size):
    n = block_size - len(input_arr) % block_size
    pad_arr=np.pad(input_arr, (0, block_size), 'constant')
    if n == block_size:
        return pad_arr
    return np.concatenate((pad_arr, np.ones(n)))
def encrypt(pub_key, input_arr):
    ntru = NtruCipher(167, 3, 128)
    ntru.h_poly = Poly(pub_key, x).set_domain(ZZ)
    input_arr = padding_encode(input_arr, ntru.N)
    input_arr = input_arr.reshape((-1, ntru.N))
    output = np.array([])
    for i, b in enumerate(input_arr, start=1):
        next_output = (ntru.encrypt(Poly(b[::-1], x).set_domain(ZZ),
                                    random_poly(ntru.N, int(math.sqrt(ntru.q)))).all_coeffs()[::-1])
        if len(next_output) < ntru.N:
            next_output = np.pad(next_output, (0, ntru.N - len(next_output)), 'constant')
        output = np.concatenate((output, next_output))
    return np.array(list(map(np.int8, output)))

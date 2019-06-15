from NTRU_cryptosystem.ntrucipher import NtruCipher
from sympy.abc import x
from sympy import ZZ, Poly
import numpy as np
def padding_decode(input_arr, block_size):
    last_block = input_arr[-block_size:]
    zeros_to_remove = len(np.trim_zeros(last_block))
    return input_arr[:-(block_size + zeros_to_remove)]
def decrypt(priv_key_f,priv_key_f_p, input_arr):
    ntru = NtruCipher(167, 3, 128)
    ntru.f_poly = Poly(priv_key_f, x).set_domain(ZZ)
    ntru.f_p_poly =Poly(priv_key_f_p, x).set_domain(ZZ)
    input_arr = input_arr.reshape((-1, ntru.N))
    output = np.array([])
    for i, b in enumerate(input_arr, start=1):
        next_output = ntru.decrypt(Poly(b[::-1], x).set_domain(ZZ)).all_coeffs()[::-1]
        if len(next_output) < ntru.N:
            next_output = np.pad(next_output, (0, ntru.N - len(next_output)), 'constant')
        output = np.concatenate((output, next_output))
    return padding_decode(output, ntru.N)

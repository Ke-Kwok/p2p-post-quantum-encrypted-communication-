import math
from sympy import GF, invert
import numpy as np
from sympy.abc import x
from sympy import ZZ, Poly

def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_2_power(n):
    return n != 0 and (n & (n - 1) == 0)


def random_poly(length, d, neg_ones_diff=0):
    return Poly(np.random.permutation(
        np.concatenate((np.zeros(length - 2 * d - neg_ones_diff), np.ones(d), -np.ones(d + neg_ones_diff)))),
        x).set_domain(ZZ)


def invert_poly(f_poly, R_poly, p):
    inv_poly = None
    if is_prime(p):
        inv_poly = invert(f_poly, R_poly, domain=GF(p))
    elif is_2_power(p):
        inv_poly = invert(f_poly, R_poly, domain=GF(2))
        e = int(math.log(p, 2))
        for i in range(1, e):
            inv_poly = ((2 * inv_poly - f_poly * inv_poly ** 2) % R_poly).trunc(p)
    else:
        raise Exception("Cannot invert polynomial in Z_{}".format(p))
    return inv_poly


class NtruCipher:
    N = None
    p = None
    q = None
    df=61
    dg=20
    f_poly = None
    g_poly = None
    h_poly = None
    f_p_poly = None
    f_q_poly = None
    R_poly = None

    def __init__(self, N, p, q):
        self.N = N
        self.p = p
        self.q = q
        self.R_poly = Poly(x ** N - 1, x).set_domain(ZZ)

    def generate_random_keys(self):

        while self.f_p_poly==None or self.f_q_poly==None:
            self.f_poly = random_poly(self.N, self.df, neg_ones_diff=-1)
            try:
                self.generate_f_key()
            except:
                continue

        self.g_poly = random_poly(self.N,self.dg)
        self.h_poly = ((self.p * self.f_q_poly * self.g_poly) % self.R_poly).trunc(self.q)

    def generate_f_key(self):
        self.f_p_poly = invert_poly(self.f_poly, self.R_poly, self.p)
        self.f_q_poly = invert_poly(self.f_poly, self.R_poly, self.q)


def generate():
    N = 167
    p = 3
    q = 128
    ntru = NtruCipher(N, p, q)
    ntru.generate_random_keys()
    h = ntru.h_poly.all_coeffs()[::-1]
    f= ntru.f_poly.all_coeffs()[::-1]
    f_p= ntru.f_p_poly.all_coeffs()[::-1]
    priv_key_f=np.array(f).astype(np.int8)[::-1]
    priv_key_f_p=np.array(f_p).astype(np.int8)[::-1]
    pub_key=np.array(h).astype(np.int8)[::-1]
    return priv_key_f,priv_key_f_p,pub_key



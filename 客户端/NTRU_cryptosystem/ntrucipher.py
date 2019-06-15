from sympy.abc import x
from sympy import ZZ, Poly
class NtruCipher:
    N = None
    p = None
    q = None
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
    def encrypt(self, msg_poly, rand_poly):
        return (((rand_poly * self.h_poly).trunc(self.q) + msg_poly) % self.R_poly).trunc(self.q)
    def decrypt(self, msg_poly):
        a_poly = ((self.f_poly * msg_poly) % self.R_poly).trunc(self.q)
        b_poly = a_poly.trunc(self.p)
        return ((self.f_p_poly * b_poly) % self.R_poly).trunc(self.p)

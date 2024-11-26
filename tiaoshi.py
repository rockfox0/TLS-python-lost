import math
import random

class Alice:
    p=0
    q=0
    p = 0
    q = 0
    N = 0
    R = 0
    M = []
    def __init__(self, p,q,R):
        self.p = p
        self.q = q
        self.N = p * q
        self.R = R


class Bob:
    M = ''
    PK = {
        "R": 0,
        "N": 0
    }
    C = []

    def __init__(self, R, N):
        self.PK['R'] = R
        self.PK['N'] = N
def Ec(self,M):
    C=[]
    for i,m in enumerate(M):
        c=0
        randomnum = random.randint(1, 20000)
        if m == '1':
            c = (self.PK['R'] * (randomnum ** 2)) % self.PK["N"]
        else:
            c = (randomnum ** 2) % self.PK["N"]
        C.append(c)
        return C

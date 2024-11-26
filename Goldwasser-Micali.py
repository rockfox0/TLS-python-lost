import math
import random


class Alice:
    p = 0
    q = 0
    N = 0
    R = 0
    M = []

    def __init__(self, p, q, R):
        self.p = p
        self.q = q
        self.N = p * q
        self.R = R

    # 解密
    def Dc(self, eM):
        self.M = []
        for i, em in enumerate(eM):
            temp = '0'
            c = int(math.sqrt(em % self.N))
            # a = int(math.sqrt(em % self.q))
            # 判断加密后的数组元素a, (a mod p) and (a mod q)是否是二次剩余
            if c ** 2 == em:
                temp = '0'
            # if c ** 2 != em and a ** 2 != em:
            else:
                temp = '1'
            self.M.append(temp)
        return self.M


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

    # 加密
    def Ec(self, M):
        C = []
        for i, m in enumerate(M):
            c = 0
            # 产生一个随机数，要满足randomnum是mod N的二次剩余
            randomnum = random.randint(1, 20000)
            if m == '1':
                c = (self.PK['R'] * (randomnum ** 2)) % self.PK["N"]
            else:
                c = (randomnum ** 2) % self.PK["N"]
            C.append(c)
        return C


# 验证同态性质
def testTong(a, b, n):
    result = []
    for i in range(len(a)):
        result.append((a[i] * b[i]) % n)
    return result


if __name__ == '__main__':
    p, q, R = 232312311797, 971179711797, 17
    a = "1011011000111110000110"  #

    b = "0011011000101110000111"  #

    alice = Alice(p, q, R)
    bob = Bob(R, p * q)
    aa = bob.Ec(a)
    alice.Dc(aa)
    bb = bob.Ec(b)
    print("aa: " + str(aa))
    print("bb: " + str(bb))
    print("Dc(aa): " + str(alice.Dc(aa)))
    print("Dc(bb): " + str(alice.Dc(bb)))
    # 验证加密后的数据是否具有异或同态性质
    temp = testTong(aa, bb, p * q)
    print("temp: " + str(temp))
    print("Dc(temp): " + str(alice.Dc(temp)))


import random
import math

from Crypto.Util.number import getPrime

p=getPrime(256)
q=getPrime(256)
# 判断 x 是否是模 n 的二次剩余
def is_quadratic_residue(x, p):
    return pow(x, (p - 1) // 2, p) == 1


# 自动生成素数 p, q 和公钥 N, y
def generate_keys(bit_length=64):
    def generate_prime():
        while True:
            candidate = random.getrandbits(bit_length)
            if candidate % 2 != 0 and all(candidate % i != 0 for i in range(3, int(math.sqrt(candidate)) + 1, 2)):
                return candidate

    # 随机生成素数 p 和 q
    p, q = generate_prime(), generate_prime()
    while p == q:
        q = generate_prime()

    N = p * q

    # 随机生成一个 R，使 y = R^2 mod N 是非二次剩余
    while True:
        R = random.randint(2, N - 1)
        y = pow(R, 2, N)
        if not is_quadratic_residue(y, p) and not is_quadratic_residue(y, q):
            break

    return (p, q, N, y)


# 加密函数
def encrypt(message, N, y):
    ciphertext = []
    for bit in message:
        r = random.randint(2, N - 1)
        if bit == 0:
            c = pow(r, 2, N)  # 二次剩余
        else:
            c = (pow(r, 2, N) * y) % N  # 非二次剩余
        ciphertext.append(c)
    return ciphertext


# 解密函数
def decrypt(ciphertext, p, q):
    decrypted_message = []
    for c in ciphertext:
        # 判断 c 是否是模 p 和模 q 的二次剩余
        if is_quadratic_residue(c, p) and is_quadratic_residue(c, q):
            decrypted_message.append(0)
        else:
            decrypted_message.append(1)
    return decrypted_message


# 测试 GM 加密算法
if __name__ == "__main__":
    # 自动生成密钥
    bit_length = 16  # 素数位数
    p, q, N, y = generate_keys(bit_length)

    print("Generated Keys:")
    print(f"p = {p}, q = {q}, N = {N}, y = {y}")

    # 明文消息 (以二进制比特流表示)
    message = [1, 0, 1, 1, 0]

    # 加密
    print("\nOriginal Message:", message)
    ciphertext = encrypt(message, N, y)
    print("Ciphertext:", ciphertext)

    # 解密
    decrypted_message = decrypt(ciphertext, p, q)
    print("Decrypted Message:", decrypted_message)

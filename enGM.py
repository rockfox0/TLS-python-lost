import random
def encrypt(N,R, message):
    encrypted_message = []
    for bit in message:
        random_num = random.randint(1, N - 1)
        if bit == '0':
            c = pow(random_num, 2, N)
        elif bit == '1':
            c = (R * pow(random_num, 2,N)) % N
        encrypted_message.append(c)
    return encrypted_message
import socket
import hashlib
from enGM import encrypt
from AES import *
# 公钥参数
e = 65537  # 公钥指数
n = 6136679291682810841556532139529343013591813977703808764043702615336288554376265811871960372534506419617688578092169859617955296838114938189837606356594307  # RSA模数
def string_to_binary(input_string):
    return ''.join(format(ord(c), '08b') for c in input_string)
# 验证签名并提取 server_key
def verify_certificate():
    # 连接到服务端
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.168.152", 9001))  # 替换为实际服务器IP和端口

    # 接收证书数据
    certificate_data = client.recv(4096).decode()
    print("Received Certificate:\n", certificate_data)

    # 解析证书内容
    lines = [line.strip() for line in certificate_data.strip().split("\n") if line.strip()]
    data = lines[0].split(": ", 1)[1]
    server_key_N = int(lines[1].split(": ", 1)[1])
    server_key_R = int(lines[2].split(": ", 1)[1])
    received_data_hash = lines[3].split(": ", 1)[1]
    signature_N = int(lines[4].split(": ", 1)[1])
    signature_R = int(lines[5].split(": ", 1)[1])

    # 初始化验证标志
    a, b, c = 0, 0, 0

    # 验证 server_key_N 的签名  # 解密签名
    print(signature_N)
    decrypted_signature_N=pow(signature_N,e,n)
    server_key_N_hash = hashlib.sha256(str(server_key_N).encode()).hexdigest()  # 计算 server_key_N 的哈希值
    print(server_key_N)
    if hex(decrypted_signature_N)[2:] == server_key_N_hash:
        print("Server Key N Signature is VALID.")
        c = 1
    else:
        print("Server Key N Signature is INVALID.")

    # 验证 server_key_R 的签名
    decrypted_signature_R = pow(signature_R, e, n)  # 解密签名
    server_key_R_hash = hashlib.sha256(str(server_key_R).encode()).hexdigest()  # 计算 server_key_R 的哈希值

    if hex(decrypted_signature_R)[2:] == server_key_R_hash:
        print("Server Key R Signature is VALID.")
        b = 1
    else:
        print("Server Key R Signature is INVALID.")

    # 验证 data 的哈希值
    data_hash = hashlib.sha256(data.encode()).hexdigest()

    if data_hash == received_data_hash:
        print("Combined Data Hash is VALID.")
        a = 1
    else:
        print("Combined Data Hash is INVALID.")

    # 输出提取的 server_key 并执行加密
    if a == 1 and b == 1 and c == 1:
        print(f"Extracted Server Key N: {server_key_N}")
        print(f"Extracted Server Key R: {server_key_R}")

        N = server_key_N
        R = server_key_R
        key_message = "0101011101010111"
        M=string_to_binary(key_message)
        encrypted_message = encrypt(N, R, key_message)
        print("Encrypted Message:", encrypted_message)

        # 发送加密后的消息给服务器
        client.send(str(encrypted_message).encode())
        print("Encrypted message sent to the server.")
        talk="wuuconixwuuconix"
        message = "Hello, Server!"

        # 使用AES加密消息
        ciphertext = aes_encrypt(talk, key_message)
        print(f"Encrypted message: {encrypted_message}")

        # 发送加密消息到服务器
        client.send(str(encrypted_message).encode())
    client.close()

if __name__ == "__main__":
    verify_certificate()




import socket
from deGM import *  # 假设其中包含 RSA 解密的相关函数
from rsacrt import encrypt  # 假设包含加密函数
import ast
from AES import *  # 假设包含 AES 加解密相关函数

# 假设已经有 p, q 作为私钥参数
p = ...
q = ...

# 服务端发送数据并接收加密消息
def server_send():
    # 构建证书数据
    certificate = """
Data: woyeaiwanyuanshen
Server Key N: 66183997670897701799014974307111979912751860284867355719449155401868664268597
Server Key R: 15913285910396832035039977691847947286083900499554735544413064739607871259108
Data Hash (SHA-256): 10c698a1fdac5f91f6e50eee11d3406ebce718a0887384fb33c1d5b927762ca0
Server Key N Signature (RSA): 72660486182249706751184101360049118482933414366254367558178374144353612018403762750258224742589645472834852185116876885659909889797030364388399210160839
Server Key R Signature (RSA): 2691504884048611146945708477262348163967115835060513626470544001554239594081978651547028128798504987428698458309466645812996677395419568126008937067323053
    """

    # 初始化服务器
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.168.152", 9001))  # 绑定到特定的IP和端口
    server.listen(1)  # 设置最大连接数为1
    print("Server is listening on port 9001...")

    # 等待客户端连接
    conn, addr = server.accept()
    print("Connection from:", addr)

    # 发送证书数据
    conn.send(certificate.encode())  # 发送证书数据（编码为字节）
    print("Certificate sent to client.")

    # 接收加密的RSA密钥消息
    message = conn.recv(4096)  # 接收来自客户端的数据
    # 将字节数据解码为字符串，然后将字符串转换为列表
    decoded_data = message.decode('utf-8')

    # 使用 ast.literal_eval() 将字符串转为列表
    M = ast.literal_eval(decoded_data)  # 这是AES加密的密钥（或者是RSA加密的内容）

    print("Received encrypted RSA message from client:", M)

    # 使用RSA解密得到的密钥
    real_key = decrypt(p, q, M)
    print("Decrypted RSA key:", real_key)


    ciphertext = conn.recv(4096)  # 接收来自客户端的AES加密消息
    cipher_text = ciphertext.decode('utf-8')
    print(f"Received encrypted message from client: {cipher_text}")

    # 解密 AES 消息
    decrypted_text = aes_decrypt(cipher_text, real_key)
    print("Decrypted AES message:", decrypted_text)

    conn.close()  # 关闭与客户端的连接

if __name__ == "__main__":
    server_send()

import hashlib

# 给定 RSA 参数
n = 6136679291682810841556532139529343013591813977703808764043702615336288554376265811871960372534506419617688578092169859617955296838114938189837606356594307
d = 4223022659793624501490754833037419624227395370469227692118513022440249230241882110907807047788396740959716212788509113265747241290035191504557922245773473
e = 65537  # 公钥指数

# 给定 GM 加密的公钥参数
server_keyN = 66183997670897701799014974307111979912751860284867355719449155401868664268597  # N
server_keyR = 15913285910396832035039977691847947286083900499554735544413064739607871259108  # R

# 给定数据
data = "woyeaiwanyuanshen"

# 计算 data 的 SHA-256 哈希值
data_hash = hashlib.sha256(data.encode()).hexdigest()

# 计算 server_keyN 和 server_keyR 的 SHA-256 哈希值
server_keyN_hash = hashlib.sha256(str(server_keyN).encode()).digest()
server_keyR_hash = hashlib.sha256(str(server_keyR).encode()).digest()

# 对 server_keyN 和 server_keyR 的哈希值分别进行 RSA 签名
server_keyN_hash_int = int.from_bytes(server_keyN_hash, byteorder='big')
server_keyR_hash_int = int.from_bytes(server_keyR_hash, byteorder='big')

# 分别对 N 和 R 的哈希值进行签名
signature_N = pow(server_keyN_hash_int, d, n)  # 用私钥 (d, n) 签名
signature_R = pow(server_keyR_hash_int, d, n)  # 用私钥 (d, n) 签名

# 整合所有数据
certificate_info = {
    "data": data,
    "server_keyN": server_keyN,  # 传递 N 部分
    "server_keyR": server_keyR,  # 传递 R 部分
    "data_hash": data_hash,
    "server_keyN_signature": signature_N,
    "server_keyR_signature": signature_R
}

# 格式化输出整合后的证书信息
certificate_str = f"""
-----BEGIN CERTIFICATE-----
Data: {certificate_info["data"]}
Server Key N: {certificate_info["server_keyN"]}
Server Key R: {certificate_info["server_keyR"]}
Data Hash (SHA-256): {certificate_info["data_hash"]}
Server Key N Signature (RSA): {certificate_info["server_keyN_signature"]}
Server Key R Signature (RSA): {certificate_info["server_keyR_signature"]}
-----END CERTIFICATE-----
"""

# 输出证书内容
print("Certificate Content:\n", certificate_str)

# 可将证书保存为文件
certificate_file_path = "D:\wdnmd\TLS3\TLScert\server_certificate.pem"
with open(certificate_file_path, "w") as cert_file:
    cert_file.write(certificate_str)

print(f"Certificate has been saved to {certificate_file_path}")

p = 217506677195547845716778556794282515709
q = 304284900694774740106060648173318087833
def decrypt(p, q, ciphertext):
    decrypted_message = []
    for c in ciphertext:
        if pow(c, (p - 1) // 2, p) == 1 and pow(c, (q - 1) // 2, q) == 1:  # 检查是否是二次剩余
            decrypted_message.append('0')
        else:
            decrypted_message.append('1')
    return ''.join(decrypted_message)

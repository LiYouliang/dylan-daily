# -*- coding: utf-8 -*-
import rsa
import base64

# 导入密钥
with open('public.pem', 'r') as f:
    RSA.importKey
    pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

with open('private.pem', 'r') as f:
    privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

# 明文
message = 'hello'

# 公钥加密
crypto = rsa.encrypt(message.encode(), pubkey)
# print(crypto)

# 私钥解密
message = rsa.decrypt(crypto, privkey).decode()
# print(message)


# 私钥签名
signature = rsa.sign(message.encode(), privkey, 'SHA-1')
# print(signature)

# 公钥验证
res = rsa.verify(message.encode(), signature, pubkey)
print(res)

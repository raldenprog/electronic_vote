from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random


import rsa


# key generation Alisa
e_private = RSA.generate(2048)
# f = open('c:\cipher\\alisaprivatekey.txt','wb')
# f.write(bytes(privatekey.exportKey('PEM'))); f.close()
e_public = e_private.publickey()

plaintext = 'hello Alisa!'.encode('utf8')
sessionkey = Random.new().read(32)
iv = Random.new().read(16) # 128 bit
obj = AES.new(sessionkey, AES.MODE_CFB, iv)
ciphertext = iv + obj.encrypt(plaintext)
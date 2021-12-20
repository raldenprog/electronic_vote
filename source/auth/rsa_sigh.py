from Crypto.PublicKey import RSA

# RSASSA-PKCS1-v1_5
# https://datatracker.ietf.org/doc/html/rfc8017#section-8.2
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

private_key = RSA.generate(2048)
public_key = private_key.publickey()

message = b'test'
hash_msg = SHA256.new(message)
signature = pkcs1_15.new(private_key).sign(hash_msg)

pkcs1_15.new(public_key).verify(SHA256.new(b'123'), signature)

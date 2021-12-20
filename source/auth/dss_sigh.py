
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256


key = DSA.generate(2048)
print(key.export_key())
publickey = key.publickey()
print(publickey.export_key())
message = b"Hello"
hash_obj = SHA256.new(message)
signer = DSS.new(key, 'fips-186-3')
signature = signer.sign(hash_obj)
pkey = DSS.new(publickey, 'fips-186-3')


hash_obj = SHA256.new(b'asdad')
pkey.verify(hash_obj, signature)

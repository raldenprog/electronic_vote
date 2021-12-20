from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP, Salsa20
from Crypto.Hash import SHA256
from Crypto.Cipher import DES
from Crypto.Cipher import AES
import zlib


def encrypt(message):
    encrypt_key = RSA.generate(2048)
    encrypted_message = PKCS1_OAEP.new(encrypt_key).encrypt(message)
    return encrypt_key, encrypted_message


def decrypt(encrypt_key, message):
    return PKCS1_OAEP.new(encrypt_key).decrypt(message)


def sign(encrypted_2_message):
    hash_encrypted_2_message = SHA256.new(encrypted_2_message)
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    signature = pkcs1_15.new(private_key).sign(hash_encrypted_2_message)
    return private_key, public_key, signature


def check_sign(encrypted_2_message, public_key, sign):
    """Проверка подписи от пользоваетеля регистратором"""
    hash_encrypted_message = SHA256.new(encrypted_2_message)
    pkcs1_15.new(public_key).verify(hash_encrypted_message, sign)


# Делает пользователь
message = b'test'

encrypt_key, encrypted_message = encrypt(message)
private_key_user, public_key_user, sign_user = sign(encrypted_message)

# Делает регистратор
check_sign(encrypted_message, public_key_user, sign_user)
private_key_registrator, public_key_registrator, sign_registrator = sign(encrypted_message)

# Делает пользователь
# message = PKCS1_OAEP.new(encrypt_key).decrypt(encrypted_message)

# Делает учитыватель
check_sign(encrypted_message, public_key_user, sign_user)
check_sign(encrypted_message, public_key_registrator, sign_registrator)

# Учитыватель получает секретный ключ для расшифровки от пользователя
decrypt(encrypt_key, encrypted_message)
print(message)

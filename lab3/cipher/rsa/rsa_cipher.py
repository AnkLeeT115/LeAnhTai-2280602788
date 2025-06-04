import rsa
import os

# Tạo thư mục chứa khóa nếu chưa tồn tại
KEY_FOLDER = 'cipher/rsa/keys'
if not os.path.exists(KEY_FOLDER):
    os.makedirs(KEY_FOLDER)

class RSACipher:
    def __init__(self):
        pass

    def generate_keys(self):
        (public_key, private_key) = rsa.newkeys(1024)
        with open(f'{KEY_FOLDER}/publicKey.pem', 'wb') as p:
            p.write(public_key.save_pkcs1('PEM'))
        with open(f'{KEY_FOLDER}/privateKey.pem', 'wb') as p:
            p.write(private_key.save_pkcs1('PEM'))

    def load_keys(self):
        if not os.path.exists(f'{KEY_FOLDER}/publicKey.pem') or not os.path.exists(f'{KEY_FOLDER}/privateKey.pem'):
            raise FileNotFoundError("Key files not found. Please generate keys first.")
        with open(f'{KEY_FOLDER}/publicKey.pem', 'rb') as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())
        with open(f'{KEY_FOLDER}/privateKey.pem', 'rb') as p:
            private_key = rsa.PrivateKey.load_pkcs1(p.read())
        return private_key, public_key

    def encrypt(self, message, key):
        return rsa.encrypt(message.encode('ascii'), key)

    def decrypt(self, ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('ascii')
        except:
            return False

    def sign(self, message, key):
        return rsa.sign(message.encode('ascii'), key, 'SHA-1')

    def verify(self, message, signature, key):
        try:
            return rsa.verify(message.encode('ascii'), signature, key) == 'SHA-1'
        except:
            return False

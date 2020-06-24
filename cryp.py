from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.utils import hashes
from cryptography.hazmat.primitives import serialization


class cryptography():

    def __init__(self, destinekey):
        self.__destine_public_key = serialization.load_pem_public_key(destinekey, backend=default_backend())

    def encryptmsg(self, msg):
        encrypted = self.__destine_public_key.encrypt(msg, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        return encrypted

    def decryptmsg(self, msg):

        with open("private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

        original_message = private_key.decrypt(msg, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return original_message.decode("utf-8")

    @staticmethod
    def getfromfile():
        try:

            with open("public_key.pem", "rb") as key_file:
                pem = key_file.read()
            return pem

        except FileNotFoundError:

            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048,backend=default_backend())
            public_key = private_key.public_key()

            pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())

            with open('private_key.pem', 'wb') as f:
                f.write(pem)

            pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

            with open('public_key.pem', 'wb') as f:
                f.write(pem)

            return pem

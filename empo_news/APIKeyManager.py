import base64
import binascii
import hashlib


class APIKeyManager:
    @staticmethod
    def get_hash_key(key):
        key_bytes = key.encode("utf-8")
        salt = base64.b64encode(key_bytes)
        salt_half_length = len(salt) // 2
        salt = salt[:salt_half_length]
        hash_bytes = hashlib.pbkdf2_hmac("sha256", key_bytes, salt, 100000)
        hash_key = binascii.hexlify(hash_bytes)
        return hash_key
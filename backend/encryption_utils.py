import os

def generate_key():
    """Generate a random 256-bit encryption key."""
    return os.urandom(32).hex()

def encrypt_data(data, key):
    """Encrypt data using a simple XOR method (just for demonstration)."""
    encrypted_data = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key))
    return encrypted_data

def decrypt_data(data, key):
    """Decrypt data using a simple XOR method (just for demonstration)."""
    decrypted_data = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key))
    return decrypted_data


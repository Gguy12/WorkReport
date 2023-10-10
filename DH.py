import random
import hashlib
import base64

prime = 1111111

def get_private_key():
    """creats a private key"""
    return random.randint(1, prime)

def get_public_key(private_key,base = 5):
    """creats a public key from the private one base variable can change"""
    return pow(16,private_key,prime)

def get_shared_key(public_key : int,private_key : int):
    """creats shared key from a public and a private key"""
    key = (public_key ** private_key) % prime
    
    return  convert_to_fernet_key(key)



def convert_to_fernet_key(input_data):
    # Convert the input to a string
    input_str = str(input_data)

    # Use a cryptographic hash function (SHA-256) to derive a 32-byte key
    sha256_hash = hashlib.sha256(input_str.encode())
    key = sha256_hash.digest()

    # Encode the bytes in URL-safe base64 format to make it a valid Fernet key
    fernet_key = base64.urlsafe_b64encode(key)

    return bytes(fernet_key)

a_priv = get_private_key()
a_pub = get_public_key(a_priv)

b_priv = get_private_key()
b_pub = get_public_key(b_priv)

if get_shared_key(a_pub,b_priv) == get_shared_key(b_pub,a_priv):
    print("Diffie Helman protocol is working!")
else:
    print("an error has happened with the Diffie Helman Protocol")


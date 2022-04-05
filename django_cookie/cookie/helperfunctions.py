# Fernet module is imported from the
# cryptography package
from cryptography.fernet import Fernet

# key is generated
def keygen():
    key = Fernet.generate_key()
    print("Key used =", key)
    return key


# Generating Fernet encryption function from key
def generateFernet(key):
    f = Fernet(key)
    return f


# the plaintext is converted to ciphertext
def encrypt(f, message):
    token = f.encrypt(message)
    # print("Ciphertext =", token)
    return token


# decrypting the ciphertext
def decrypt(f, token):
    d = f.decrypt(token)
    # print(d)
    return d


# f = keygen()
# token = encrypt(f, b"welcome to geeksforgeeks")
# d = decrypt(f, token)

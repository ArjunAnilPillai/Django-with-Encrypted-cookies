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


# f = generateFernet(b"9jRsOPoL9LCzCxlYQY7udcBuS0qwseQVFjLhQGU7mDc=")
# token = encrypt(f, b"welcome to geeksforgeeks")
# d = decrypt(
#     f,
#     b"gAAAAABiTtLJOB32ugQiZ-NJkWyXWBjWo_i26TZbHlg2DMmQ9nc69R20EQ5T_Crz7hAGJJrdycS5L49l8gZlUgWyAGTvP7hCnq8EVaCGCLx-X5w8OZAk6U0=",
# )
# print(d)

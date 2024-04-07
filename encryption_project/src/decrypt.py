import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import InvalidToken
import base64

# Determine the base directory
base_dir = os.path.join(os.path.dirname(__file__), '../data')

# Load the salt from the file
salt_path = os.path.join(base_dir, 'salt')
with open(salt_path, 'rb') as salt_file:
    salt = salt_file.read()

# Ask for the password
password = input("Enter the password for decryption: ").encode()

# Derive the key from the password
kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))

# Fernet initialization with the loaded key
cipher_suite = Fernet(key)

# Load the encrypted message from the file
encrypted_message_path = os.path.join(base_dir, 'encrypted_message.txt')
try:
    with open(encrypted_message_path, 'rb') as encrypted_file:
        encrypted_message = encrypted_file.read()

    # decrypt the message
    decrypted_message = cipher_suite.decrypt(encrypted_message)
    print(decrypted_message.decode())
    print("Decryption Successful")

except InvalidToken:
    # This block is executed if the password was incorrect
    print("Wrong password")
    print("Decryption Unsuccessful")
    


import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64

# Determine the base directory
base_dir = os.path.join(os.path.dirname(__file__), '../data')

# Ensure the base directory exists
os.makedirs(base_dir, exist_ok=True)

# Ask for the password
password = input("Enter the password for encryption: ").encode()

# Generate a salt
salt = os.urandom(16)

# Derive a key from the password
kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))

# Fernet initialization with the generated key
cipher_suite = Fernet(key)

# Ask for a secret message
message= input("Enter the message to encrypt: ")
message = message.encode()

# Encrypt the message
encrypted_message = cipher_suite.encrypt(message)

# Save the encrypted message to a file
encrypted_message_path = os.path.join(base_dir, 'encrypted_message.txt')
with open(encrypted_message_path, 'wb') as encrypted_file:
    encrypted_file.write(encrypted_message)

# Save the salt to a file for decryption
salt_path = os.path.join(base_dir, 'salt')
with open(salt_path, 'wb') as salt_file:
    salt_file.write(salt)

print("Encryption Successful")
import random
from socket import *


def modexp(base, exponent, modulus):
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result


def generate_keys(p, g):
    """Generates a new secret key and corresponding public key"""
    b = random.randint(2, p-1)
    B = modexp(g, b, p)
    return b, B

def read_private_key(path):
    """Reads the client's private key from file, or generates a new one if it doesn't exist"""
    try:
        with open(path, "r") as f:
            b = int(f.read())
    except FileNotFoundError:
        b, B = generate_keys(p, g)
        with open(path, "w") as f:
            f.write(str(b))
        with open("C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/public_key.txt", "w") as f:
            f.write(str(B))
    return b

def read_public_key(path):
    """Reads the server's public key from file"""
    with open(path, "r") as f:
        A = int(f.read())
    return A

def encrypt(msg, A, b, p):
    """Encrypts a message using the client's private key and the server's public key"""
    encrypted_msg = b""
    for ch in msg:
        encrypted_msg += bytes([ord(ch) ^ modexp(A, b, p) % 256])
    return encrypted_msg

def decrypt(msg, s):
    """Decrypts a message using the shared secret s"""
    decrypted_msg = ""
    for ch in msg:
        decrypted_msg += chr(ch ^ s % 256)
    return decrypted_msg

# Generate a large prime number p
p = 15485863

# Generate a primitive root g modulo p
g = 2

# Read the client's private key
b = read_private_key('C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/private_key.txt')

# Read the server's public key A
A = read_public_key('C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/public_key.txt')

# Initialize the client socket and connect to the server
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Send the client's public key B to the server
B = modexp(g, b, p)
client_socket.send(str(B).encode())

# Receive server's public key A
A = int(client_socket.recv(1024).decode())

# Calculate shared secret s = A**b mod p
s = modexp(A, b, p)

# Print the shared secret s
print('Shared secret:', s)

while True:
    # Send message to server
    msg = input("Enter message: ")
    
    # Encrypt message using client's private key and server's public key
    encrypted_msg = encrypt(msg, A, b, p)
    client_socket.send(encrypted_msg)
    
    # Receive response from server
    encrypted_response = client_socket.recv(1024)
    decrypted_response = decrypt(encrypted_response, s)
    print(decrypted_response)

    if msg == "exit":
        break

# Close the socket
client_socket.close()

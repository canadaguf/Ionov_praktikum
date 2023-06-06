from socket import *
import random


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
    a = random.randint(2, p-1)
    A = modexp(g, a, p)
    return a, A

def read_private_key(path):
    """Reads the server's private key from file, or generates a new one if it doesn't exist"""
    try:
        with open(path, "r") as f:
            a = int(f.read())
    except FileNotFoundError:
        a, A = generate_keys(p, g)
        with open(path, "w") as f:
            f.write(str(a))
        with open("C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/server_public_key.txt", "w") as f:
            f.write(str(A))
    return a

def read_public_key(path):
    """Reads the server's public key from file"""
    with open(path, "r") as f:
        A = int(f.read())
    return A

def encrypt(msg, B, a, p):
    """Encrypts a message using the client's public key and the server's private key"""
    encrypted_msg = b""
    for ch in msg:
        encrypted_msg += bytes([ord(ch) ^ modexp(B, a, p) % 256])
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

# Read the server's private key
a = read_private_key("C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/server_private_key.txt")

# Read the server's public key A
A = read_public_key("C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/server_public_key.txt")

# Initialize the server socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 12345))
server_socket.listen(1)
print('Server is listening...')

# Accept client connection
client_socket, address = server_socket.accept()
print('Connected by', address)

# Send the server's public key A to the client
client_socket.send(str(A).encode())

# Calculate shared secret s = B**a mod p
B = int(client_socket.recv(1024).decode())
s = modexp(B, a, p)

# Wait for incoming messages and send back responses
while True:
    # Receive message from client
    encrypted_msg = client_socket.recv(1024)
    if not encrypted_msg:
        break
    
    # Decrypt message using shared secret s
    decrypted_msg = decrypt(encrypted_msg, s)
        
    # Print received message
    print(f"Received message: {decrypted_msg}")
    
    if decrypted_msg == "exit":
        break
    
    # Send back an encrypted echo of the received message
    msg = input("Enter response: ")
    
    # Encrypt response using client's public key and server's private key
    encrypted_echo = encrypt(msg, B, a, p)

    client_socket.send(encrypted_echo)

# Close the sockets
client_socket.close()
server_socket.close()

# Print the shared secret s
print('Shared secret:', s)

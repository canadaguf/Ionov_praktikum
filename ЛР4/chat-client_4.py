import socket
import getpass

# Prompt for user input of server IP address and port number
SERVER_IP = input("Enter server IP address (default: 127.0.0.1): ") or '127.0.0.1' # Default value set to localhost
SERVER_PORT = input("Enter server port number (default: 9090): ") or 9090 # Default value set to 9090
# Secure entry of server port number
while True:
    try:
        SERVER_PORT = int(SERVER_PORT)
        break
    except ValueError:
        print("Invalid input! Please enter a valid integer port number.")
        SERVER_PORT = getpass.getpass(prompt="Enter server port number: ")

print("\nConnecting to server...")

# Create a TCP socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
except ConnectionRefusedError:
    # Handle case where server is not running
    print("Could not connect to server. Make sure the server is running and try again.")
    exit()

print(f"Connected to {SERVER_IP}:{SERVER_PORT}.")

# Receive a greeting from the server
try:
    greeting = client_socket.recv(1024).decode()
except ConnectionAbortedError:
    # Handle case where the connection was closed by the server
    print("Server closed the connection unexpectedly.")
    client_socket.close()
    exit()

if greeting == "What is your name?":
    # Prompt the user to input their name and send it back to the server
    name = input("Enter your name: ")
    client_socket.send(name.encode())
else:
    print(greeting)

# Continuously send and receive messages
while True:
    # Read a string input from the user
    message = input("Enter a message to send to the server (or type 'exit' to quit): ")

    if message == "exit":
        # Send exit message to server and close the socket
        client_socket.send(message.encode())
        client_socket.close()
        print("Connection closed.")
        break

    # Send the message to the server
    client_socket.send(message.encode())
    print("Message sent to server.")

    # Receive data from the server
    data = client_socket.recv(1024).decode()
    print(f"Received data from server: {data}")


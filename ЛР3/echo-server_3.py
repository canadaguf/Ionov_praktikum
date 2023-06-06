import socket
import getpass
import logging
            
                
HOST = input("Enter host name (default: 127.0.0.1): ") or '127.0.0.1' # Default value set to localhost
PORT = input("Enter port number (default: 9090): ") or 9090 # Default value set to 9090
# Secure entry of port number
while True:
    try:
        PORT = int(PORT)
        break
    except ValueError:
        print("Invalid input! Please enter a valid integer port number.")
        PORT = getpass.getpass(prompt="Enter port number: ")

# Set up logging to a file
logging.basicConfig(filename='C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/server.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(f"Starting server on {HOST}:{PORT}...")
print(f"Starting server on {HOST}:{PORT}...")

# Load previous identity data from file
identities = {}
try:
    with open('C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/identity.txt', 'r') as f:
        for line in f:
            ip, name = line.strip().split(',')
            identities[ip] = name
except FileNotFoundError:
    pass

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            logging.info(f"Server listening on {HOST}:{PORT}...")
        except OSError:
            # If the port is busy, increment it and try again
            logging.warning(f"Port {PORT} is busy. Trying another port...")
            PORT += 1
            continue
        
        s.listen()
        conn, addr = s.accept()
        logging.info(f"Client connected from {addr[0]}:{addr[1]}")
        ip = addr[0]

        with conn:
            logging.info("Connection established.")
            if ip in identities:
                # Known identity, greet by name
                name = identities[ip]
                conn.sendall(f"Welcome back, {name}!".encode())
                logging.info(f"Greeted {ip} as {name}.")
            else:
                # Unknown identity, query for name and write to file
                conn.sendall(b"What is your name?")
                name = conn.recv(1024).decode()
                identities[ip] = name
                with open('C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/identity.txt', 'a') as f:
                    f.write(f"{ip},{name}\n")
                logging.info(f"Recorded new identity: {ip} as {name}.")
                conn.sendall(f"Welcome, {name}!".encode())
                
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    logging.info("No more data from client. Disconnecting...")
                    break
                    
                logging.info(f"Received data: {data}")
                conn.sendall(data.encode())
                logging.info("Data sent back to client.")
                
        logging.info("Client disconnected. Waiting for new connections...")

logging.info("Shutting down server.")

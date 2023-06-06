'''
This is chat-server
'''
import socket
import threading
import getpass
import logging
import queue
import time

def write_message_history(message):
    with open('C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/message_history.txt', 'a') as f:
        f.write(message)

def handle_client(conn, addr, identities, message_history_lock, message_history, clients):
    ip = addr[0]
    with conn:
        logging.info("Connection established.")
        if ip in identities:
            # Known identity, greet by name
            name = identities[ip]
            conn.sendall(f"Welcome back, {name}!\n".encode())
            logging.info(f"Greeted {ip} as {name}.")
        else:
            # Unknown identity, query for name and write to file
            conn.sendall(b"What is your name?\n")
            name = conn.recv(1024).decode().strip()
            identities[ip] = name
            with open('C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/identity.txt', 'a') as f:
                f.write(f"{ip},{name}\n")
            logging.info(f"Recorded new identity: {ip} as {name}.")
            conn.sendall(f"Welcome, {name}!\n".encode())

        # # Send message history to new client
        # with message_history_lock:
        #     conn.sendall(f"HISTORY: {message_history}".encode())

        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                logging.info("No more data from client. Disconnecting...")
                break

            logging.info(f"Received data: {data}")

            # Add message to history
            message = f"[{name}]: {data}\n"
            with message_history_lock:
                message_history += message

            # Write message history to file
            write_message_history(message)

            # Broadcast message to all clients
            for client_socket in clients.values():
                client_socket.sendall(message.encode())

            logging.info("Data broadcast to all clients.")

    # Remove client from dictionary of active clients
    with clients_lock:
        del clients[ip]

    logging.info("Client disconnected. Waiting for new connections...")

def listen_for_clients(s, q):
    s.listen()
    while True:
        try:
            conn, addr = s.accept()
            q.put((conn, addr))
            logging.info(f"Client connected from {addr[0]}:{addr[1]}")
        except Exception as e:
            logging.error(f"Error accepting connection: {e}")

def receive_messages(client_socket, message_history):
    while True:
        try:
            # Receive data from the server
           data = conn.recv(1024).decode().strip()
           if not data:
               logging.info("No more data from client. Disconnecting...")
               break

           logging.info(f"Received data: {data}")

           # Add message to history
           message = f"[{name}]: {data}\n"
           with message_history_lock:
               message_history += message

           # Write message history to file
           write_message_history(message)

           # Broadcast message to all clients
           for client_socket in clients.values():
               client_socket.sendall(message.encode())

           logging.info("Data broadcast to all clients.")
        except ConnectionResetError:
            # Handle case where the connection was closed by the server
            print("Server closed the connection unexpectedly.")
            client_socket.close()
            exit()

if __name__ == '__main__':
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
    
    # Initialize message history
    message_history = ""
    
    # Initialize dictionary to store connected clients and the lock for accessing it
    clients = {}
    clients_lock = threading.Lock()
    
    # Initialize lock for shared access to message history
    message_history_lock = threading.Lock()
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            logging.info(f"Server listening on {HOST}:{PORT}...")
            print(f"Server listening on {HOST}:{PORT}...")
    
            # Start thread to listen for incoming connections
            q = queue.Queue()
            t = threading.Thread(target=listen_for_clients, args=(s, q))
            t.daemon = True
            t.start()
    
            while True:
                # Check for new clients and spawn threads to handle them
                while not q.empty():
                    conn, addr = q.get()
                    # Store a reference to the client socket object
                    with clients_lock:
                        clients[addr[0]] = conn
                    client_thread = threading.Thread(target=handle_client, args=(conn, addr, identities, message_history_lock, message_history, clients))
                    client_thread.start()
    
                # Wait briefly before checking again
                time.sleep(0.1)
    
                # Create a separate thread for each client to receive messages from the server
                with clients_lock:
                    for client_socket in clients.values():
                        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, message_history))
                        receive_thread.start()
    
    except OSError:
        logging.error(f"Port {PORT} is already in use. Please choose another port.")
        print(f"Port {PORT} is already in use. Please choose another port.")
        exit()
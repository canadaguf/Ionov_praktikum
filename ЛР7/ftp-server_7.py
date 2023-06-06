import socket
import os

PORT = 9090

# Set the directory that the user is allowed to access
root_dir = 'C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/'
os.chdir(root_dir)

# Open log files for different actions
conn_log = open('C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/connections.log', 'a')
auth_log = open('C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/authorizations.log', 'a')
file_op_log = open('C:/Users/Ilya/Desktop/university/4 семестр/Практикум по програмированию/file_operations.log', 'a')

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

def process(req):
    if req == 'pwd':
        return os.getcwd()
    elif req == 'ls':
        return '; '.join(os.listdir())
    elif req.startswith('mkdir'):
        foldername = req.split()[1]
        os.mkdir(os.path.join(root_dir, foldername))
        return f"Folder '{foldername}' created successfully"
    elif req.startswith('rmdir'):
        foldername = req.split()[1]
        os.rmdir(os.path.join(root_dir, foldername))
        return f"Folder '{foldername}' deleted successfully"
    elif req.startswith('rm'):
        filename = req.split()[1]
        os.remove(os.path.join(root_dir, filename))
        return f"File '{filename}' deleted successfully"
    elif req.startswith('rename'):
        oldname, newname = req.split()[1:]
        os.rename(os.path.join(root_dir, oldname), os.path.join(root_dir, newname))
        return f"File '{oldname}' renamed to '{newname}' successfully"
    elif req.startswith('upload'):
        filename = req.split()[1]
        with open(os.path.join(root_dir, filename), 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
        return f"File '{filename}' uploaded successfully"
    elif req.startswith('download'):
        filename = req.split()[1]
        with open(os.path.join(root_dir, filename), 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                conn.sendall(data)
        return f"File '{filename}' downloaded successfully"
    elif req.startswith('cd'):
        # Check that the requested directory is inside the root directory
        new_dir = os.path.abspath(os.path.join(os.getcwd(), req.split()[1]))
        if not new_dir.startswith(root_dir):
            return "Access denied"
        os.chdir(new_dir)
        return f"Changed directory to '{new_dir}'"
    elif req == 'exit':
        return 'Goodbye!'
    else:
        return 'Bad request'

# Loop for accepting connections and processing requests
while True:
    print("Listening on port", PORT)
    conn, addr = sock.accept()
    print("Connected by", addr)

    request = conn.recv(1024).decode()
    print("Request:", request)

    # Write log messages to their respective log files
    if request == "exit":
        conn_log.write(f"Connection closed by {addr}\n")
    else:
        conn_log.write(f"Connected by {addr}\n")

    if request.startswith("login") or request.startswith("register"):
        auth_log.write(f"{request} by {addr}\n")

    if request.startswith("mkdir") or request.startswith("rmdir") or request.startswith("rm") or \
            request.startswith("rename") or request.startswith("upload") or request.startswith("download") or \
            request.startswith("cd"):
        file_op_log.write(f"{request} by {addr}\n")

    # Process request and send response
    response = process(request)
    conn.send(response.encode())

    if request == 'exit':
        break

# Close log files and socket connection
conn_log.close()
auth_log.close()
file_op_log.close()
sock.close()

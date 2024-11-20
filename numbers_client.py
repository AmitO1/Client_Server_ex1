import socket
import sys

def sendall(sock, data):
    """Send all data over a socket connection."""
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent
    
def receive_message(sock):
    message = b''
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        message += chunk
        if b'\n' in chunk:
            break
    return message.decode('utf-8').strip()
        
HOST = "localhost"
PORT = 1337
loogged_in = False
username = ""

if len(sys.argv) == 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
if len(sys.argv) == 2:
    port_check = int(sys.argv[1])
    if 0 <= port_check <= 65535:
        print("Cannot enter only port number without hostname!")
        sys.exit(1)
    else:
        HOST = sys.argv[1]

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect((HOST,PORT))
data = receive_message(clientSock)
while clientSock.fileno() != -1:
    if data == "Hi "+username+", good to see you.":
        loogged_in = True
        print(data)
        
    if data == "Failed to login.":
        print(data)
        
    if data == "Welcome! Please log in.":
        print(data)
        
    if loogged_in == False:
        username = input()
        if username == "quit":
            sendall(clientSock, b'quit')
            clientSock.close()
            break
        else:
            password = input()
        if password == "quit":
            sendall(clientSock, b'quit')
            clientSock.close()
            break
        user_pass = username+", "+password+"\n"
        if "User: " in username:
            username = username.split(": ")[1] #will be handeled on server side more here only for login message constraction
        sendall(clientSock, user_pass.encode())
        data = receive_message(clientSock)
    else:
        message = input()
        message = message + "\n"
        command = message.split(" ")
        sendall(clientSock,message.encode())
        data = receive_message(clientSock)
        if data == "Closing connection...":
            print(data)
            clientSock.close()
        elif data == "error: result is too big":
            print(data)
        elif data != "Unkown command, Closing connection":
            if command[0] == "calculate:":
                print(f"Response: {data}.")
            if command[0] == "max:":
                print(f"the maximum is {data}")
            if command[0] == "factors:":
                print(f"the prime factors of {command[1][:-1]} are: {data}")
        else:
            print(data)
            clientSock.close()
        
    



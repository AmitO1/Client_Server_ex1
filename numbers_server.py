import socket
import select
import sys

def check_user(username, password):
    if username in user_pass and user_pass[username] == password:
        return True
    else:
        return False

#returns true if number is bigger or smaller then number in int32 range 
def is_outside_int32_range(num):
    INT32_MIN = -2**31  
    INT32_MAX = 2**31 - 1  
    return num < INT32_MIN or num > INT32_MAX

def parse_data(data):
    splited_data = data.split(" ")
    
    if splited_data[0] == "calculate:":
        if len(splited_data) != 4:
            return "unknown command"
        if splited_data[2] == "+":
            number = int(splited_data[1]) + int(splited_data[3])
            if is_outside_int32_range(number):
                return "error: result is too big"
            return str(number)
        elif splited_data[2] == "-":
            number = int(splited_data[1]) - int(splited_data[3])
            if is_outside_int32_range(number):
                return "error: result is too big"
            return str(number)
        elif splited_data[2] == "*":
            number = int(splited_data[1]) * int(splited_data[3])
            if is_outside_int32_range(number):
                return "error: result is too big"
            return str(number)
        elif splited_data[2] == "/":
            number = round(int(splited_data[1]) / int(splited_data[3]),2)
            if is_outside_int32_range(number):
                return "error: result is too big"
            return str(number)
        elif splited_data[2] == "^":
            number = int(splited_data[1]) ** (int(splited_data[3]))
            if is_outside_int32_range(number):
                return "error: result is too big"
            return str(number)
        else:
            return "unknown command"
        
    elif splited_data[0] == "max:":
        if len(splited_data) < 3:
            return "unknown command"
        max = int((splited_data[1])[1:])
        for i in range(2 , len(splited_data)):
            if (i == len(splited_data) - 1):
                num = int((splited_data[i])[:-1])
                if num > max:
                    max = num
            else:
                num = int(splited_data[i])
                if num > max:
                    max = num
                    
        return str(max)  
    
    elif splited_data[0] == "factors:":
        if len(splited_data) != 2:
            return "unknown command"
        num = int(splited_data[1])
        return prime_factors(num)
        
    else:
        return "unknown command"
    
def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    i = 3
    while i * i <= n: 
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2  
    
    if n > 2:
        factors.append(n)
        
    return ' '.join(map(str, sorted(factors))) 
        
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

file = open("/Users/amitomer/Desktop/לימודים/networks/ex1/users_file.txt","r")

user_pass = {}
for line  in file:
    splited = line.split("\t")
    username = splited[0]
    password = splited[1].replace("\n","")
    user_pass[username] = password

file.close()
HOST = ""
PORT = 1337


serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((HOST,PORT))
serverSock.listen()
serverSock.setblocking(0)

socket_list = [serverSock]
connected_socket_list = []
responses = {}

while True:
    readable, writeable, _ = select.select(socket_list, socket_list, [])
    for sock in readable:
        if sock == serverSock:
            connectionSock, addr = serverSock.accept()
            print(f"Connection from: {connectionSock} has been established")
            connectionSock.setblocking(0)
            if connectionSock not in socket_list:
                socket_list.append(connectionSock)
                response = "Welcome! Please log in.\n"
                responses[connectionSock] = []
                responses[connectionSock].append(response.encode())
        else:
            if sock not in connected_socket_list:
                data = receive_message(sock)
                if data == "quit": # in case quitting before plugin username and password
                    socket_list.remove(sock)
                    del responses[sock]
                    sock.close()
                    break # socket still not in connected socket list so can just break
                else:
                    parts = data.split(", ")
                    if len(parts) != 2:
                        response = "Failed to login.\n"
                        responses[sock].append(response.encode())
                    if "User: " not in parts[0] or "Password: " not in parts[1]:
                        response = "Failed to login.\n"
                        responses[sock].append(response.encode())
                    else: 
                        result = [parts[0].split(": ")[1], parts[1].split(": ")[1]]
                        if check_user(result[0], result[1]):
                            meesage = "Hi "+result[0]+", good to see you.\n"
                            connected_socket_list.append(sock)
                            responses[sock].append(meesage.encode())
                        else:
                            response = "Failed to login.\n"
                            responses[sock].append(response.encode())
            else: 
                data_after = receive_message(sock)
                if data_after != "":
                    if data_after == "quit":
                        response = "Closing connection...\n"
                        responses[sock].append(response.encode())
                        break
                    result = parse_data(data_after)
                    if result == "unknown command":
                        response = "Unkown command, Closing connection\n"
                        responses[sock].append(response.encode())
                    else:
                        result = result + "\n"
                        responses[sock].append(result.encode())
    for sock in writeable:
        if sock in responses and responses[sock]:
            response = responses[sock][0]
            sendall(sock,response)
            if response.decode() == "Unkown command, Closing connection\n" or response.decode() == "Closing connection...\n":
                # handle disconnection due to unkown command / quit command
                connected_socket_list.remove(sock)
                socket_list.remove(sock)
                del responses[sock]
                sock.close()
            else:
                responses[sock].pop(0)
            
            
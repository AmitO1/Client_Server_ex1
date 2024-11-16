few key points:
1. validity of message is handled on server side excpet of some minor things handled in both
    server and client just for validation on client side
2. added sendall and recieve message (acted like recieve all end in \n)
3. client can send any type of message to server but the connection will end in case of an unkown command
    or in case of known command with incorrect number of paramter or incorrect syntex

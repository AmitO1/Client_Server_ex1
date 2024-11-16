few key points:
1. validity of message is handled on server side excpet of some minor things handled in both
    server and client just for validation on client side
2. added sendall and recieve message (acted like recieve all end in \n)
3. client can send any type of message to server but the connection will end in case of an unkown command
    or in case of known command with incorrect number of paramter or incorrect syntex
4. for valid login: User: username then enter and Password: password
5. only in login incorrect input will not cause disconnection from the server in any other command 
    input of the wrong format will cause disconnection (implemented this that way because that what i understood from assignment)
6. command list:
    calculate: X Y Z (x,z are integers and z is one of {+,-,^,*,/})
    max: (X1 X2 X3 .... Xn) (X1,...,Xn are integers)
    factors: X (X is an integer)
    quit (to close connection from user side also possible while trying to login)
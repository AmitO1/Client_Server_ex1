Server - Client description:
1. Upon connection you will recieve the message: "Welcome! Please log in."
2. To login first write: User: username , then press enter and then Password: password.
3. Upon wrong information or format in login you will recieve the message: "Failed to login."
   you can try loggin in as many times as you want and can also enter quit instead of User \ Password
   in order to quit and close the connection.
4. After loggin in the server support the follwing commands:
   calculate: X Y Z (X,Z are intergers and Z is one of the follwing: +,-,^,/,*)
   max: (X1 X2 ... Xn) (X1,...,Xn are integers)
   factors: X (X is an integer)
   quit (to close connection)
   in case of wrong format for any of the command above or unkown command server will close the connection
   and you will recieve a message.
5.  In order to implement client side other then whats given make sure that any message you send ends with
    \n because recieve_message function in server side will look for \n (I am aware it might be problematic but for the current assignment due to short messages and responses need to implemented I figured a line would be enough for sending and recieving a full message)
6.  Same goes to server side in order to communicate with the client meesages sent must end with \n. 
import socket

HOST=''
PORT=5061

class ServerConnection:

    def __init__(self):
        self._socket_active = False
        self.sock_con=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print('Socket created')

        self.__open_socket()


    def close_socket(self):
        if self.is_active() == True:
            self._socket_active = False
            self.sock_con.close()
        else:
            print('Socket already closed!')


    def __open_socket(self):
            try:
                self.sock_con.bind((HOST,PORT))
                print('Socket bind complete')
            except:
                print('**Err: Socket bind unsuccessfully')
            try:
                self.sock_con.listen(1)
                self._socket_active = True
                print('Socket now listening')
            except:
                print('**Err: Socket could not listening')


    def is_active(self):
        return self._socket_active

    
    
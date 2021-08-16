
import socket
import sys
import pickle
import numpy as np
import struct ## new
import zlib
from server_connection import ServerConnection
import cv2 as cv
import PIL



class Server:

    def __init__(self):
    
        self.con = ServerConnection()
        if self.con.is_active():
            self.acception_loop()
        else:
            print("** Server could not establish the connection!")
            exit(1)


    def acception_loop(self):
        while True:
            conn,addr=self.con.sock_con.accept()
            print(f"Socket: {conn}, address: {addr}, connect to the Server successfully!")
            self.handle_communication(conn, addr)
            print('Socket now listening')

    def handle_communication(self, conn, addr):

        # Initiate communication's arguments
        ### data = b""
        u_long_size = struct.calcsize(">L")
        char_size = struct.calcsize(">c")
        payload_size = u_long_size + char_size
        print(f"payload_size: {payload_size}")
        # Message structure : first {u_long_size} bytes represent the data size, 
        # The {char_size} bytes represent the message type and the rest the data
        while True:
            ret_val = self.handle_message(conn, addr, u_long_size,char_size)
            if ret_val[0]:
                self.reply(conn, addr)
            else:
                print(ret_val[1])
                conn.close()
                break


    def handle_message(self, conn, addr, u_long_size,char_size):
        data = b""
        payload_size = u_long_size + char_size
        # receive the message's info part
        while len(data) < payload_size :
            # -------- add try/except in cases that the client shut-down the connection ------
            print(f"Recv: {len(data)}")
            data += conn.recv(4096)
            # To avoid infitiy loop
            if len(data) == 0:
                return [False,"**Err: receiving a message"] 
    
        print(f"Done Recv: {len(data)}")
        # Decode message info
        packed_msg_size = data[:u_long_size]
        packed_msg_type = data[u_long_size: payload_size]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        msg_type = struct.unpack(">c", packed_msg_type)[0].decode('ascii')
        
        # Update data var 
        data = data[payload_size:]
        print(f"msg_type: {msg_type}")
        # receive the data
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]            
        # Update data var to the next round
        data = data[msg_size:]

        func_dict = {'0': self.handle_img, '1': self.handle_str}

        if msg_type in func_dict.keys():
            return func_dict[msg_type](frame_data)
        return [False, "**Err: undefined message type"]


    def reply(self, conn, addr):
        conn.send(bytes("Message received", "utf-8"))


    def handle_img(self, frame_data):
        print('image received')
        pil_image = pickle.loads(frame_data)
        opencvImage = cv.cvtColor(np.array(pil_image), cv.COLOR_RGB2BGR)
        cv.imshow('frame', opencvImage)
        cv.waitKey(1)
        return [True]
        pass

    def handle_str(self, frame_data):
        print('string received')
        return [True]
        pass
        

        
Server()

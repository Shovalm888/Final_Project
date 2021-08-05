import cv2
import io
import socket
import struct
import time
import pickle
import zlib

HOST= socket.gethostname()
PORT = 5061


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320);
cam.set(4, 240);

img_counter = 0
cv2.waitKey(0)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True and img_counter < 100:
    ret, frame = cam.read()
    # result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    # client_socket.send(pickle.dumps(Message('image', size, frame).encode_msg()))
    client_socket.sendall(struct.pack(">L", size) + struct.pack(">c", '0'.encode('ascii')) +  data)
    img_counter += 1

cam.release()
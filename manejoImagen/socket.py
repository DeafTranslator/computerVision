import socket 
import base64
import sys
import time
from datetime import timedelta

file = "A-test10.jpg"

# with open(file, "rb") as imageFile:
#   img = base64.b64encode(imageFile.read())
#   img = "image-?" + img + "-?" + file
#   print (img)

ip = "10.28.236.86"
port = 6781
message = "Hello, Server"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

start_time = time.time()
print("\nstart time " + str(start_time))
clientSocket.sendto('klk',(ip, port))
data, addr = clientSocket.recvfrom(10000)
end_time = time.time()
print("\nend time " + str(end_time))
diff = end_time - start_time
print(data)
print("Time elapsed: " + str(timedelta(seconds=int(round(diff)))))
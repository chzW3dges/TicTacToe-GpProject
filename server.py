import socket
import sys
from threading import Thread

#sini letak board fx


#socket fx
def start():
   port = 8888

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   print("\n||||||              Welcome to the Server            ||||||\n")

   try:
     s.bind(("", port))
   except socket.error as e:
     print("Bind failed. Got a socket error! " + str(e))
     sys.exit()

   print("Listening from clients...")
   s.listen(3)

   while True:
     connection, address = s.accept()
     ip, port = str(address[0]), str(address[1])
     print("-- Connected with " + ip + ":  --" + port)

     try:
         Thread(target = c, args=(connection, ip, port)).start()
     except socket.error as e:
         print("-- Thread did not start! --" + str(e))
         s.close()

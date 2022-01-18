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
         Thread(target = client, args=(connection, ip, port)).start()
     except socket.error as e:
         print("-- Thread did not start! --" + str(e))
         s.close()

#bagitau player no bape yg dh connect
def client(c, ip, port):
   global game, num2Eng, available
   player.append(port)
   print ("Player " + str(len(player_list)) + "port: " + str(port))


#kat client tanya nak start game ke tak
   while True:
        data = c.recv(2048)
        data = data.decode('utf-8')
        if not data:
            print('break')
            break
        print("from connected user: " + str(data))
        if (data == "Yes" or 'Y' or 'y' or "yes"):
            game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            num2Eng = {0: ' ', 1: 'O', 4: 'X'}
            available = [(x, y) for x in range(3) for y in range(3)]
            startGame(c, ip)
        elif (data == "No" or 'N' or 'n' or "no"):
            break


#print board
def printBoard():
    s = ''
    for x in range(5):
        s += ' '
        for y in range(3):
            if x % 2 == 0:
                s += ' ' + num2Eng[board[x // 2][j]] + ' '
                if y == 0 or y == 1: s += '|'
            else:
                s += '--- '
        s += '\n'
    return s

#print contoh board nk tunjuk kt player
def printBnum():
    s = ''
    for x in range(5):
        s += ' '
        for y in range(3):
            if x % 2 == 0:
                s += ' ' + str(((x // 2) * 3) + y + 1) + ' '
                if y == 0 or y == 1: s += '|'
            else:
                s += '--- '
        s += '\n'
    return s


if __name__ == "__main__":
    start()

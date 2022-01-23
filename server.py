import socket
import sys
from threading import Thread

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
   s.listen(3)   # listen from client 

   while True:
     connection, address = s.accept()
     ip, port = str(address[0]), str(address[1])
     print("-- Connected with " + ip + ":  --" + port)

     try:
         Thread(target = client, args=(connection, ip, port)).start()
     except socket.error as e:
         print("-- Thread did not start! --" + str(e))
         s.close()

#this is board fx
game = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
num2Eng = {0: ' ', 1: 'O', 4: 'X'}
available = [(x, y) for x in range(3) for y in range(3)]
#recv x or o
pointcalc = {(x * 3) + y + 1: (x, y) for x in range(3) for y in range(3)}
player = []



#function for client
def client(c, ip, port):
   global game, num2Eng, available
   player.append(port)
   print ("Player " + str(len(player)) + " port: " + str(port))


#for client to ask whether to start the game or not? 
   while True:
        data = c.recv(1024)
        data = data.decode('utf-8')
        if not data:
            print('break')
            break
        print("Player confirmation: " + str(data))
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
                s += ' ' + num2Eng[game[x // 2][y]] + ' '
                if y == 0 or y == 1: s += '|'
            else:
                s += '--- '
        s += '\n'
    return s

#print the board to show to the player or user 
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


#function ambik kira how to win!!
def checkWin():   
    if len(available) == 0:
        return "Draw"
    col = [0, 0, 0]
    diag = [0, 0]
    for x in range(3):
        if sum(game[x]) == 3:
            return 'O Win!'
        elif sum(game[x]) == 12:
            return 'X Win!'
        for y in range(3):
            if x == y:
                diag[0] += game[x][y]
            if x + y == 2:
                diag[1] += game[x][y]
            col[y] += game[x][y]
    for i in range(3):
        if col[x] == 3:
            return 'O Win!'
        elif col[x] == 12:
            return 'X Win!'
    for x in range(2):
        if diag[x] == 3:
            return 'O Win!'
        elif diag[x] == 12:
            return 'X Win!'
    return 'No'



#function player make a move
def playerMove(player, data):   
    x = int(data[0])
    y = int(data[1])

    if player == 4:
        print("X at", x, y)
    else:
        print("O at", x, y)
    game[x][y] = player
    available.pop(available.index((x, y)))




#function when start the game
def startGame(conn, ip):   
    message = printBnum() + "\n\nDo you want to be O or X? [O/X]: "
    conn.send(message.encode())
    data = conn.recv(2048).decode()
    print(ip[0] + " is", data)
    if data.upper() == 'X':
        player1 = 4
        player2 = 1
    else:
        player2 = 4
        player1 = 1

    data = ""
    while checkWin() == 'No':
        if (data != 'r'):
            s = printBoard()
            conn.send(s.encode())
        data = conn.recv(1024).decode()

        if data == 'r':
            conn.send(printBoard().encode())
            if checkWin() != 'No':
                break
        else:
            data = pointcalc[int(data)]
            playerMove(player1, data)
            if checkWin() != 'No':
                break

    message = printBoard() + '\n\n' + checkWin()
    conn.send(message.encode())

if __name__ == "__main__":
    start()

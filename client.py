import socket
import sys
import os

Client = socket.socket()
host = '192.168.56.102'
port = 8888
os.system('clear')


try:
    Client.connect((host, port))
except socket.error as e:
    print(str(e))
    print("Connection error")
    sys.exit()

print("\n=================================================")
print("\n                 TIC - TAC - TOE")
print("\n=================================================")

#Ask client if they want to start the game
while True:
    response = input('\nWould you like to start the game?[Yes/No]: ')
    if response.upper() in ('YES','Y'):
        break
        
    if response.upper() in ('NO,'N'):
        Client.close()
        sys.exit()

#Ask client to choose between X or O!
while response.upper() != 'NO' or response.upper() != 'N':
    Client.send(response.encode())
    data = Client.recv(1024).decode()
    while True:
        print("\n" + data)
        player = input()
        if player.upper() in ('O', 'X'):
            break
        print('\nPlease enter either O or X!')
    Client.send(player.encode())
    data = Client.recv(1024).decode()
    
    #Ask client to place X and O on the board
    while "Win" not in data:
        print("\nBoard:\n" + data)
        while True:
            response = input('Your turn. \nEnter number 1-9 to choose your position [(c) - display board]\n')
            if response in [str(i+1) for i in range(9)] + ['c']:
                break
        Client.send(response.encode())
        data = Client.recv(1024).decode()
        if data == "Win":
            break
    print("\nGame Over.")
    print(data)

    #Ask client whether they want to play again
    print("\n=================================================")
    response = input("Would you like to play again?[Yes/No]: ")
    if response.upper() == "NO" or response.upper() == 'N':
        print("Thanks for playing!")
        Client.close()
        sys.exit()

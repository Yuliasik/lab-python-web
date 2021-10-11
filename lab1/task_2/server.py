import threading
import socket

host = '127.0.0.1'
port = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Start the server
server.bind((host, port))
server.listen()

clients = []
nicknames = []


# send messages to each client
def broadcast(message):
    for client in clients:
        client.send(message)


# handle what will happens when new user connected
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            # send messages to each users
            broadcast(message)
        except Exception:
            # get index of current user
            index = clients.index(client)
            # remove this user from clients list
            clients.remove(client)
            # close connection with current user
            client.close()
            # get nickname of the user to send notification to other users
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


# what will happens when connection from new user received
def receive():
    while True:
        # get client and address from connection
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # send message to new user for inputing his nickname
        client.send('NICK~'.encode('ascii'))
        # receive nickname from user, add mickname and client to lists
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # message to server about nickname
        print(f'Nickname of the client is {nickname}!')
        # notification to each users that new user joined
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        # message to new user that he was connected
        client.send('Connected to the server'.encode('ascii'))
        # start new thread with handle this user
        threading.Thread(target=handle, args=(client,)).start()


print("Server is runned...")
receive()

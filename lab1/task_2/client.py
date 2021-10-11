import threading
import socket

nickname = input('Choose a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 55556
# connect to the server
client.connect((host, port))

# what will happens when any message is received
def receive():
    while True:
        try:
            # if message is NICK~ send chosen username to the server 
            message = client.recv(1024).decode('ascii')
            if message == "NICK~":
                client.send(nickname.encode('ascii'))
            # else print this message to chat
            else:
                print(message)
        except Exception:
            print("An error occurred!")
            client.close()
            break


# what happens when user send message pushing enter button
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


# thread for receiving of messages from the server
threading.Thread(target=receive).start()
# thread for sending of messages to the server
threading.Thread(target=write).start()

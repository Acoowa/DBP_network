import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 12345

nickname = input('Enter your nickname: ')
print('Enter ":q" to quit')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive(client) -> None:
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(nickname.encode())
            else:
                print(message)
        except Exception as e:
            print(f'Error: {type(e).__name__}, {e}')
            client.close()
            break


def write(client) -> None:
    while True:
        message = input('')
        if message == ':q':
            client.send(message.encode())
            client.close()
            break
        client.send(f'{nickname}: {message}'.encode())

        if not client:
            break


t_receive = Thread(target=receive, args=(client,))
t_receive.start()

write(client)

import socket
from threading import Thread
import sys

HOST = '127.0.0.1'
PORT = 12345

nickname = input('Enter your nickname: ')
print('Enter "q" to quit')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive() -> None:
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except Exception as e:
            print(f'Error: {type(e).__name__}, {e}')
            client.close()
            break
    client.close()


t_receive = Thread(target=receive)
t_receive.start()

while True:
    to_send = input('')
    if to_send == 'q':
        client.send(to_send.encode())
        break
    client.send(f'{nickname}: {to_send}'.encode())

client.close()

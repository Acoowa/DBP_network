import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

nickname = input('Enter your nickname: ')
print('Enter ":q" to quit')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive() -> None:
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


def write() -> None:
    while True:
        message = input('')
        if message == ':q':
            client.close()
            return
        client.send(f'{nickname}: {message}'.encode())


t_receive = threading.Thread(target=receive)
t_receive.start()

t_write = threading.Thread(target=write)
t_write.start()

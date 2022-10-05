from multiprocessing import Process
import socket


def fib(n):
    if n < 2:
        return n

    a, b = 0, 1

    for i in range(n):
        a, b = b, a+b

    return a


def handle_client(c: socket.socket):
    print('Got client')
    while True:
        try:
            c.send('>'.encode('utf-8'))
            data = c.recv(1024)

            try:
                num = int(data.decode('utf-8'))
            except ValueError:
                c.send('Invalid input !\n'.encode('utf-8'))
                continue

            fib_num = fib(num)
            c.send(f'= {fib_num}\n'.encode('utf-8'))
        except ConnectionError:
            break


def main():
    sock = socket.socket()
    sock.bind(('', 9001))
    sock.listen(100)

    while True:
        c, addr = sock.accept()
        print('Starting process for', f'{addr[0]}:{addr[1]}')
        p = Process(target=handle_client, args=(c,))
        p.start()


if __name__ == '__main__':
    main()

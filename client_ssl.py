import socket
import ssl
from time import sleep
import multiprocessing
from random import randint

from server_ssl import CRT_PATH


def create_socket_pool():
    pool = multiprocessing.Pool(processes=4)
    sleep_time_list = [randint(3, 10) for x in range(4)]
    pool.map(socket_connect, sleep_time_list)


def socket_connect(sleep_time):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ssl.wrap_socket(s,
                           ca_certs=CRT_PATH,
                           cert_reqs=ssl.CERT_REQUIRED)

    sock.connect(("localhost", 9000))
    data = "Hello world"
    sleep(sleep_time)
    sock.sendall(data)
    result = sock.recv(1024)
    print result
    sock.close()


if __name__ == "__main__":
    create_socket_pool()

import multiprocessing
import socket
import ssl


"""
openssl genrsa -des3 -out server.orig.key 2048
openssl rsa -in server.orig.key -out server.key
openssl req -new -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
"""


CRT_PATH = 'server.crt'
KEY_PATH = 'server.key'


def main():
    server = ServerSSL("0.0.0.0", 9000)
    print("Listening")
    server.start()
    print("Joining processes")
    for process in multiprocessing.active_children():
        print("Joining: " + str(process))
        process.terminate()
        process.join()
    print("Server stopped")


class ServerSSL(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.socket = None

    def start(self):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.hostname, self.port))
            self.socket.listen(1)
        else:
            print("Reusing existing socket")
        print("Listening")
        self.manage_socket()

    def manage_socket(self):
        while True:
            c, address = self.socket.accept()
            conn = ssl.wrap_socket(c,
                                   server_side=True,
                                   certfile=CRT_PATH,
                                   keyfile=KEY_PATH)
            print("Connected successfully")

            proc = multiprocessing.Process(target=handle_connection, args=(conn, address))
            proc.daemon = True
            proc.start()
            print("Spawned process: " + str(proc))


def handle_connection(connection, address):
    try:
        print("Connected: {}: {}".format(connection, address))
        while True:
            data = connection.recv(1024)
            if data == "":
                print("Socket closed remotely")
                break
            print("Received: " + data)
            connection.sendall(data)
            print("Data sent")
    except socket.error:
        print("Could not handle request")
    finally:
        print("Socket closed")
        connection.close()


if __name__ == "__main__":
    main()

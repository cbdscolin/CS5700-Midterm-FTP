import socket

class SocketManager:

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("ftp.5700.network", 21))
        sock.sendall("USER dsouzaco\r\n".encode())

        data = sock.recv(4096)

        print ("Data1", data)

        sock.sendall("PASS GPjeOfuAJi7dQ0nYTpUI\r\n".encode())

        data = sock.recv(4096)

        print ("Data2", data)


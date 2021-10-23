import socket
from utils.util import Utils
import re


class FTPConnectionManager:
    MAX_MESSAGE_SIZE = 4096

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.connect(("ftp.5700.network", 21))
        self.data_socket = None
        self.init_connection()

    def init_connection(self):
        data = self.receive_control_message()
        Utils.print_logs("Pre: ", data)
        self.send_control_message("USER {}\r\n".format(self.username))

        data = self.receive_control_message()
        Utils.print_logs("Response after username is passed: ", data)

        self.send_control_message("PASS {}\r\n".format(self.password))

        data = self.receive_control_message()
        Utils.print_logs("Response after password is passed: ", data)

        self.send_control_message("TYPE I\r\n")
        data = self.receive_control_message()
        Utils.print_logs("Response after type is passed: ", data)

        self.send_control_message("MODE S\r\n")
        data = self.receive_control_message()
        Utils.print_logs("Response after mode is passed: ", data)

        self.send_control_message("STRU F\r\n")
        data = self.receive_control_message()
        Utils.print_logs("Response after stru is passed: ", data)

    def send_control_message(self, message):
        self.control_socket.sendall(message.encode())

    def receive_control_message(self):
        response = self.control_socket.recv(FTPConnectionManager.MAX_MESSAGE_SIZE)

        response_code = response.split(" ")[0]
        response_message = response[len(response_code):].strip()
        response_code = int(response_code)

        FTPConnectionManager.check_response_code(response_code)

        return response_code, response_message

    def receive_data_channel_message(self):
        response_message = self.data_socket.recv(FTPConnectionManager.MAX_MESSAGE_SIZE)
        return response_message

    def start_data_channel(self):
        self.send_control_message("PASV\r\n")
        resp_code, resp_msg = self.receive_control_message()
        Utils.print_logs("Response after requesting data channel: ", resp_code, resp_msg)

        parts = resp_msg.split(" ")
        if len(parts) != 4:
            Utils.print_logs("Invalid message received when opening data channel ")
            exit(1)
        ip_parts = parts[3].replace('(', '').replace(')', '').replace('.', '').split(",")
        ip_address = ".".join(ip_parts[:4])
        port = int(int(int(ip_parts[4]) << 8) + int(ip_parts[5]))

        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.connect((ip_address, port))


    def list_directory(self, path):
        self.start_data_channel()
        self.send_control_message("LIST {}\r\n".format(path))
        ls_response = self.receive_data_channel_message()
        Utils.print_logs("LS Command response: \n", ls_response)

    @staticmethod
    def check_response_code(response_code):
        if 400 <= response_code <= 600:
            Utils.print_logs("Error occurred")
            exit(1)

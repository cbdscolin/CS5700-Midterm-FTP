import socket
from utils.util import Utils
import re


class FTPConnectionManager:
    MAX_MESSAGE_SIZE = 4096

    # FTP_HOST = "ftp.5700.network"
    # FTP_PORT = 21
    ANONYMOUS_USERNAME = "anonymous"

    def __init__(self, username, password, host, port):
        self.username = username
        if username is None:
            self.username = FTPConnectionManager.ANONYMOUS_USERNAME 
        self.password = password
        '''
        Create a socket for control channel and connect to the FTP host & port
        '''
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.connect((host, port))
        '''
        Initialize a socket for data channel. This data socket is created later when performing ls, rm, rmdir, mkdir,
        cp & mv commands.
        '''
        self.data_socket = None
        self.init_connection()

    def init_connection(self):
        data = self.receive_control_message()
        Utils.print_logs("Pre: ", data)
        self.send_control_message("USER {}\r\n".format(self.username))

        data = self.receive_control_message()
        Utils.print_logs("Response after username is passed: ", data)

        # TODO: Verify is anonymous username works.
        if self.username is not FTPConnectionManager.ANONYMOUS_USERNAME:
            self.send_control_message("PASS {}\r\n".format(self.password))

            data = self.receive_control_message()
            Utils.print_logs("Response after password is passed: ", data)

        # Set the connection to 8-bit binary data mode
        self.send_control_message("TYPE I\r\n")
        data = self.receive_control_message()
        Utils.print_logs("Response after type is passed: ", data)

        # Set the connection to stream mode (as opposed to block or compressed)
        self.send_control_message("MODE S\r\n")
        data = self.receive_control_message()
        Utils.print_logs("Response after mode is passed: ", data)

        # Set the connection to file-oriented mode (as opposed to record- or page-oriented).
        self.send_control_message("STRU F\r\n")
        data = self.receive_control_message()
        Utils.print_logs("Response after stru is passed: ", data)

    def close_control_connection(self):
        # Send QUIT message to close the connection.
        self.send_control_message("QUIT\r\n")
        # Close the control channel socket
        self.control_socket.close()

    def close_data_connection(self):
        # Close the data channel socket once the data is sent or received.
        self.data_socket.close()
        self.data_socket = None

    def send_control_message(self, message):
        # Send a message through control channel socket
        self.control_socket.sendall(message.encode())

    def receive_control_message(self):
        # Receive a message from control channel
        response = self.control_socket.recv(FTPConnectionManager.MAX_MESSAGE_SIZE)
        '''
        Each response has a error code and the associated response message. 
        '''
        response_code = response.split(" ")[0]
        response_message = response[len(response_code):].strip()
        response_code = int(response_code)

        # Check if the request was success or failure
        FTPConnectionManager.check_response_code(response_code, response_message)

        return response_code, response_message

    def send_data_message(self, message):
        # Send message to data channel. Used when writing to a remote file.
        if self.data_socket is not None:
            self.data_socket.sendall(message)
        else:
            raise Exception("No data channel to send data")

    def receive_data_channel_message(self):
        # Received message from data channel. Used in ls, cp and mv command.
        response_message = self.data_socket.recv(FTPConnectionManager.MAX_MESSAGE_SIZE)
        return response_message

    '''
    Create a socket to read and write data from FTP data channel
    '''
    def start_data_channel(self):
        self.send_control_message("PASV\r\n")
        resp_code, resp_msg = self.receive_control_message()
        Utils.print_logs("Response after requesting data channel: ", resp_code, resp_msg)

        parts = resp_msg.split(" ")
        if len(parts) != 4:
            Utils.print_logs("Invalid message received when opening data channel ")
            exit(1)
        # Identify the IP address to be used in data channel socket
        ip_parts = parts[3].replace('(', '').replace(')', '').replace('.', '').split(",")
        ip_address = ".".join(ip_parts[:4])
        # Identify the port number to be used in data channel socket
        port = int(int(int(ip_parts[4]) << 8) + int(ip_parts[5]))

        # Create data channel socket.
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.connect((ip_address, port))

    def list_directory(self, path):
        self.start_data_channel()
        self.send_control_message("LIST {}\r\n".format(path))
        data_channel_response = self.receive_data_channel_message()
        Utils.print_logs("LS Command response: \n", data_channel_response)
        self.close_data_connection()
        self.close_control_connection()

    '''
    Creates a directory in the specified remote ftp path. First we create a data channel and send the 
    MKD message to control channel to create directory.
    '''
    def make_directory(self, path):

        self.start_data_channel()
        self.send_control_message("MKD {}\r\n".format(path))
        data_channel_response = self.receive_control_message()
        Utils.print_logs("MKDIR Command response: \n", data_channel_response)
        self.close_data_connection()

    '''
    Removes a directory from the specified remote ftp path. First we create a data channel and send the 
    RMDIR message to control channel to remove directory.
    '''
    def remove_directory(self, path):
        self.start_data_channel()
        self.send_control_message("RMD {}\r\n".format(path))
        data_channel_response = self.receive_control_message()
        Utils.print_logs("RMDIR Command response: \n", data_channel_response)
        self.close_data_connection()

    '''
    Removes a file from the specified remote ftp path. First we create a data channel and send the 
    DELE message to control channel to remove the file.
    '''
    def remove_file(self, path):
        self.start_data_channel()
        self.send_control_message("DELE {}\r\n".format(path))
        data_channel_response = self.receive_control_message()
        Utils.print_logs("RM Command response: \n", data_channel_response)
        self.close_data_connection()

    '''
    Downloads the contents of the remote file on the FTP server and saves the contents to a local file in the specified 
    location.
    '''
    def save_remote_file_to_local(self, remote_file_path, local_file_path):
        self.start_data_channel()
        self.send_control_message("RETR {}\r\n".format(remote_file_path))
        Utils.print_logs("RETR Command Control response: \n", self.receive_control_message())

        '''
        Receive the remote file contents first and after receiving the contents close the data channel.
        '''
        data_channel_response = self.receive_data_channel_message()
        self.close_data_connection()
        Utils.print_logs("RETR Command Data response: \n", data_channel_response)


        '''
        Store the remote file contents to the local file.
        '''
        Utils.save_file(local_file_path, data_channel_response)

    '''
    Uploads the contents of a local file to a remote file in the specified location in FTP server.
    '''
    def upload_file_to_remote(self, local_file_path, remote_file_path):
        self.start_data_channel()
        '''
        Send message to control channel to indicate file upload.
        '''
        self.send_control_message("STOR {}\r\n".format(remote_file_path))
        control_channel_response = self.receive_control_message()
        Utils.print_logs("RETR Command Control response: \n", control_channel_response)

        '''
        Load the contents of the local file into a buffer.
        '''
        contents = Utils.get_file_contents(local_file_path)
        '''
        Save the contents of the local file the remote FTP file and close the data connection after transfer of data
        is complete.
        '''
        self.send_data_message(contents)
        self.close_data_connection()

    '''
    Perform extensive error handling.
    '''
    @staticmethod
    def check_response_code(response_code, msg):
        # TODO: Check if other error codes should be handled differently
        if 400 <= response_code <= 600:
            Utils.print_logs("Error occurred ", msg)
            exit(1)

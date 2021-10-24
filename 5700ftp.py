from connection.connection_manager import FTPConnectionManager

class CommandParser:

    def __init__(self):
        pass

    def parse_command(self, command):
        pass




if __name__ == "__main__":
    print ("Hello!")

    username = "dsouzaco"
    password = "GPjeOfuAJi7dQ0nYTpUI"

    connection = FTPConnectionManager(username, password)
    connection.list_directory("/")

    connection = FTPConnectionManager(username, password)
    connection.make_directory("/test_dir")

    connection = FTPConnectionManager(username, password)
    connection.make_directory("/test_dir_2")

    connection = FTPConnectionManager(username, password)
    connection.remove_directory("/test_dir")

    connection = FTPConnectionManager(username, password)
    connection.upload_file_to_remote("temp-1.txt", "/test_dir_2/temp-test.txt")

    connection = FTPConnectionManager(username, password)
    connection.save_remote_file_to_local("/test_dir_2/temp-test.txt", "temp-2.txt")

    connection = FTPConnectionManager(username, password)
    connection.remove_file("/test_dir_2/temp-test.txt")

    connection = FTPConnectionManager(username, password)
    connection.remove_directory("/test_dir_2")



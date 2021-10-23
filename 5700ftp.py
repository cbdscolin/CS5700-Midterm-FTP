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

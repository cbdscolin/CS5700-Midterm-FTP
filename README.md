CS5700 Midterm Project

Members:
Colin Burtan Dsouza
John Walsh

High Level Approach:
First we scan the command line arguments to identify the username, password, FTP host and port number. We also
parse the command line arguments that consists of the command (which can be one of ls, mkdir, rmdir, rm, mv or cp)
and the arguments for the command. Next based on the command we call the respective functions which perform 
the relevant operation. For each of the commands we first create a control channel. Then we send requests
for authentication to the FTP server by using the username and password we identified before. On successful
authentication we send the following 3 requests through the control channel.
1. Request to set 8-bit binary mode for data.
2. Request to set the connection to stream mode.
3. Request to set the connection to file-oriented mode.

If all the requests are successful then we try to perform the actual operation based on the command.
If the command is "ls" we start a data channel and send "LIST" request through the FTP control channel. If the request
succeeds we obtain the information about the list of files and directories in the data channel which is printed
on the console. Then we close the control channel.

If the command is "mkdir" we send the "MKD" request through the FTP control channel. If the request succeeds then
the directory is created and we close the control channel.

If the command is "rmdir" we send the "RMD" request through the FTP control channel. If the request succeeds then
the directory is deleted and we close the control channel.

If the command is "rm" we create a data channel and then issue "DELE" request through the FTP control channel to 
delete the file. If the request is successful the file is deleted and we close the data and control channel.

If the command is "cp" we create a data channel. If the first argument to the "cp" command points to local file 
system we copy the contents of the file to a buffer. Then we issue a "STOR" request through the FTP control channel.
If the request is successful we send the contents of the buffer through the FTP data channel. Once we send the 
contents to close the data channel and control channel. 
If the first arguments to the "cp" command points to a location in the FTP server we create a data channel
and issue "RETR" request through the control channel. If the request is successful we copy the contents of the 
file to a local buffer by using the open data channel. Once the entire file contents are copied to the buffer and
socket is closed we copy the contents to the local file system and close the control.

If the command is "mv" we follow the similar procedure listed in the "cp" command but we delete the file pointed
to by the first argument for "mv" command. If the first argument points to a file in local file system then we
issue a request to delete the local file. If the first argument points to a file in remote file system then we 
issue a request to the FTP server to delete the file (Using the procedure listed for "rm" command above). 




Challenges Faced:
1. Parsing the command line arguments to obtain user name, password, FTP host port number, command and arguments.
2. Error handling when we issue commands through the control channel and performing relevant actions based on the 
   response received.




Testing:

We tested our code manually against the following cases
1. Create a directory on the FTP server using the program and manually checking if the directory is created.
2. Delete a directory on the FTP server using the program and manually checking if the directory is deleted.
3. Create a file in the local file system with some content and then copy this file to the FTP server using
   our program. We then manually verified this file exists on the FTP server. We downloaded the file contents 
   using put command and verified the contents of the file to match the contents of the uploaded file.
4. Upload a file to the FTP server as mentioned in testcase 3 to the FTP server. Then download the file to local 
   file system using our program. We then manually verified the contents of the file to match the file uploaded in
   testcase 3.
5. Upload a file to the FTP server as mentioned in testcase 3 to the FTP server. Then delete the remote file 
   using our FTP program. We manually verified that the file was deleted from the FTP server.
6. Create a few files and directories in the root folder using our FTP program. We then list the contents
   of the root folder. We verified that the output consists of all files and directories in the root folder.
7. We moved a file from local file system to FTP server. We manually verified that this file was deleted from 
   the local file system. We manually verified the contents of the file on the FTP server to match 
   the contents of the local file.
8. We moved a file from FTP server to local file system. We verified that this file was deleted from the FTP 
   server. We also verified that the contents of the local file match the contents of the FTP server.

Apart from this we also added a few automation tests to simplify the process of testing. The unit tests can be 
found in FTPTests.py. These tests use ftplib package to verify if our program executes the relevant command
as expected.


Breakdown of work:



John worked on parsing the command line arguments to obtain the username, password, FTP host, FTP port, command
and the arguments. 
Colin worked on writing functionality related to listing directories, creating and removing directories, 
uploading file to FTP server, downloading file from FTP server and deleting file on the FTP server. 

John worked on integrating this code with the code that does command line parsing (calling the relevant
functions). Colin and John worked together on fixing issues related to the code and handling possible errors.

John and Colin worked together on adding unit tests to check the functionality implemented in the program.




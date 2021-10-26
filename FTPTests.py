import os
import unittest
import ftplib


'''
Run these tests after ensuring the root FTP folder is empty. Tests may fail otherwise. Update username and password
'''
def create_test_file(filename):
    f = open(filename, "w")
    content = ""
    for r in range(100000):
        content += str(r)
    f.write(content)
    f.close()
    return content

def get_file_contents(filename):
    f = open(filename, "r")
    contents = f.read()
    return contents


class MyTestCase(unittest.TestCase):
    username = "dsouzaco"
    password = "GPjeOfuAJi7dQ0nYTpUI"
    server = "ftp.5700.network"

    def test_mkdir_rmdir(self):
        ftp = ftplib.FTP(MyTestCase.server)
        ftp.login(MyTestCase.username, MyTestCase.password)

        # Create directory
        os.popen('./5700ftp mkdir ftp://{}:{}@{}/test-dir-1/'.format(MyTestCase.username, MyTestCase.password, MyTestCase.server))

        # Test if directory is created.
        data = []
        ftp.dir(data.append)
        self.assertEqual(len(data), 1)
        self.assertTrue("test-dir-1" in data[0])

        # Delete directory
        os.popen('./5700ftp rmdir ftp://{}:{}@{}/test-dir-1/'.format(MyTestCase.username, MyTestCase.password, MyTestCase.server))

        # Test if directory is deleted.
        data = []
        ftp.dir(data.append)
        self.assertEqual(len(data), 0)

    def test_copy_and_rm(self):
        contents_orig = create_test_file("test-1.txt")
        # Copy a file to FTP server
        os.popen('./5700ftp cp ./test-1.txt ftp://{}:{}@{}/test-1.txt'.format(MyTestCase.username, MyTestCase.password, MyTestCase.server))

        ftp = ftplib.FTP(MyTestCase.server)
        ftp.login(MyTestCase.username, MyTestCase.password)

        # Copy the remote FTP file to local
        os.popen('./5700ftp cp ftp://{}:{}@{}/test-1.txt ./test-2.txt'.format(MyTestCase.username, MyTestCase.password, MyTestCase.server))

        contents_ftp = get_file_contents("test-2.txt")
        # Check if file content matches
        self.assertEqual(contents_ftp, contents_orig)

        # Cleanup FTP and local files
        ftp.delete("test-1.txt")
        os.popen("rm -rf ./test-1.txt")
        os.popen("rm -rf ./test-2.txt")

    def test_ls(self):
        create_test_file("test-1.txt")

        os.popen('./5700ftp mv ./test-1.txt ftp://{}:{}@{}/test-1.txt'.format(MyTestCase.username, MyTestCase.password, MyTestCase.server))
        os.popen('./5700ftp mkdir ftp://{}:{}@{}/dir_test_1'.format(MyTestCase.username, MyTestCase.password, MyTestCase.server))
        os.popen('./5700ftp mkdir ftp://{}:{}@{}/dir_test_2'.format(MyTestCase.username, MyTestCase.password, MyTestCase.server))

        ftp = ftplib.FTP(MyTestCase.server)
        ftp.login(MyTestCase.username, MyTestCase.password)

        # Verify ls output.
        data = []
        ftp.dir(data.append)
        self.assertEqual(len(data), 3)
        self.assertTrue("dir_test_1" in data[0])
        self.assertTrue("dir_test_2" in data[1])
        self.assertTrue("test-1.txt" in data[2])

        # Cleanup FTP and local files.
        ftp.delete("test-1.txt")
        ftp.rmd("dir_test_1")
        ftp.rmd("dir_test_2")

    def test_mv(self):
        ftp = ftplib.FTP(MyTestCase.server)
        ftp.login(MyTestCase.username, MyTestCase.password)
        create_test_file("test-1.txt")

        # Move local file to FTP
        os.popen('./5700ftp mv ./test-1.txt ftp://{}:{}@{}/test-1.txt'.format(MyTestCase.username, MyTestCase.password, MyTestCase.server))

        self.assertFalse(os.path.exists("test-1.txt"))
        data = []
        ftp.dir(data.append)
        self.assertEqual(len(data), 1)
        self.assertTrue("test-1.txt" in data[0])

        # Move FTP file to local
        os.popen('./5700ftp mv ftp://{}:{}@{}/test-1.txt ./tmp.txt'.format(MyTestCase.username, MyTestCase.password, MyTestCase.server))

        data = []
        ftp.dir(data.append)
        self.assertEqual(len(data), 0)
        self.assertTrue(os.path.exists("tmp.txt"))

        # Cleanup
        os.popen("rm -rf tmp.txt")


if __name__ == '__main__':
    unittest.main()

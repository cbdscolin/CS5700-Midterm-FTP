class Utils:

    @staticmethod
    def print_logs(*log_lines):
        res = ""
        for log in log_lines:
            res += str(log)
        print res

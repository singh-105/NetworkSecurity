import sys

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)

        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()

        if exc_tb is not None:
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.lineno = exc_tb.tb_lineno
        else:
            self.file_name = "Unknown"
            self.lineno = -1

    def __str__(self):
        return (
            f"Error occured in python script name [{self.file_name}] "
            f"line number [{self.lineno}] "
            f"error message [{self.error_message}]"
        )

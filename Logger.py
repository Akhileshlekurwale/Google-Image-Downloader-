from datetime import datetime
import logging

class Logging:
    def __init__(self,name):
        """
        This class is used for Logging the details of the process.
        :param name: name of the logger file
        """
        try:
            self.logger = logging.getLogger(name)
        except Exception as e:
            raise Exception(e)

    def initialize_logger(self):
        """
        This will add additional information to logger like formatter and hadler

        """
        try:
            if len(self.logger.handlers)==0:

                log_level = 'log_level'

                if log_level == 'ERROR':
                    self.logger.setLevel(logging.ERROR)
                elif log_level == 'DEBUG':
                    self.logger.setLevel(logging.DEBUG)

                formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

                file_handler = logging.FileHandler('Advance Image Downloader.log')

                file_handler.setFormatter(formatter)

                self.logger.addHandler(file_handler)

            return self.logger
        except Exception as e:
            raise Exception(e)

    def log_print(self,log_statement,log_level):

        try:
            if log_level== 'info':
                self.logger.info(log_statement)
            elif log_level == 'error':
                self.logger.error(log_statement)
            elif log_level == 'exception':
                self.logger.exception(log_statement)

        except Exception as e:
            raise Exception(e)







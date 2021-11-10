import smtplib
import ssl
from Logger import Logging

logger_obj = Logging("Advance Image Downloader")
logger_obj.initialize_logger()

class SendEmail:


    def __init__(self ):
        """
        Initiate email object
        """
        try:
            self.email = "datascienceinfor@gmail.com"
            self.password = "test@321"
        except Exception as e:
            logger_obj.log_print('Email.py - __init__ has exception' + str(e), 'exception')
            raise Exception(e)

    def send_notification (self,receiver_email, message):
        """
        sends email to the user
        :param receiver_email: receiver email is input eai; given by user
        :param message: text of message
        :return:
        """
        server = None
        try:
            smpt_server = 'smtp.gmail.com'
            port = 587
            context = ssl.create_default_context()

            server = smtplib.SMTP(smpt_server,port)
            server.starttls(context = context)
            server.login(self.email, self.password)
            logger_obj.log_print("Server login is successfull",'info')
            server.sendmail(self.email,receiver_email, message + '\n')
            logger_obj.log_print('Email has been sent', 'info')

        except Exception as e:
            logger_obj.log_print("send_notification has exception" +str(e), 'exception')

        finally:
            if server:
                server.close()






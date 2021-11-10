import os
import shutil
import requests

from Logger import Logging

logger_obj = Logging("Advance Image Downloader")
logger_obj.initialize_logger()

class Download:
    def __init__(self,result = None ):
        """
        It initiaate content of downloaded files
        :param result:Cassandra object of downloadable result content
        """
        try:
            self.content = result
        except Exception as e:
            logger_obj.log_print("Download.py __init__ has exception" + str(e) + "Exception")
            raise Exception(e)

    @staticmethod
    def create_dir(req_id):
        """
        This function is used to create a directory image storing
        :return:
        """
        try:
            if not os.path.exists(req_id):
                os.mkdir(req_id)
        except Exception as e:
            logger_obj.log_print("Download.py __init__ has exception" + str(e) + "Exception")
            raise Exception(e)

    def download_images(self, search_term,req_id):
        """
        :param search_term: Input term for image search given by user
        :param req_id: unique id for request
        """
        try:
            counter = 1
            for row in self.content:
                url = row.url
                req = requests.get(url, stream=True, headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                                                                              "AppleWebKit/537.36 (KHTML, like Gecko) " 
                                                                              "Chrome/95.0.4638.54 " 
                                                                              "Safari/537.36"})
                print("'counter = {} Header = {} URL ={} ".format(counter,req.headers,url))
                logger_obj.log_print('Filetype is {}'.format(req.headers['Content-Type'].split('/')[1]), 'Info')
                filetype = req.headers['Content-Type'].split('/')[1].split(';')[0]

                if filetype not in ['jpg','jpeg']:
                    filetype = 'jpeg'

                req.raw.decode_content = True
                with open(req_id + '/' + search_term + '_' + str(counter) + '.'+filetype, 'wb') as file:
                    file.write(req.content)
                    file.close()
                    counter = counter+1

        except Exception as e:
            logger_obj.log_print('Download.py - download_image has exception' + str(e), 'Exception')
            raise Exception(e)

    @staticmethod
    def create_zip(req_id):
        """
        This function will create zip file for downloaded images
        :param req_id: unique id for request
        :return:
        """
        try:
            if not os.path.exists(req_id+ '_zipfile.zip'):
                shutil.make_archive(req_id + '_zipfile', 'zip', req_id)
        except Exception as e:
            logger_obj.log_print('Download.py - create_zip' + str(e), 'Exception')
            raise Exception(e)

    @staticmethod
    def delete_file(req_id):
        """
        delete files
        """
        try:
            if os.path.exists(req_id+ '_zipfile.zip'):
                os.remove(req_id+ '_zipfile.zip')
                print('zip file deleted')

            if os.path.exists(req_id):
                shutil.rmtree(req_id)
                print('Image folder deleted')
        except Exception as e:
            logger_obj.log_print('Download.py - delete_file' + str(e), 'Exception')
            raise Exception(e)




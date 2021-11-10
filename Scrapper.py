import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from bs4 import BeautifulSoup

from Logger import Logging

chrome_options = webdriver.ChromeOptions()
#chrome_options.binary_locations = os.environ.get("GOOGLE_CHROME_BIN")
#chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('no-sandbox')
chrome_options.add_argument('disable-dev-shm-usage')

logger_obj = Logging("Advance Image Downloader")
logger_obj.initialize_logger()




class ImageScrapper:
    """ This class will have all functions for scrapping"""

    def __init__(self, count_image):
        """This function will initiate the browser """
        try:
            self.count_image = count_image
            self.browser = webdriver.Chrome(executable_path= ChromeDriverManager().install(),chrome_options=chrome_options)
        except Exception as e:
            logger_obj.log_print('(Scrapper.py(__init__) - '+str(e), 'exception')
            raise Exception(e)


    def createURL(self,keyword):
        """
        This function will open image url
        :param keyword: Keyword entered by user of which set of images required
        :return: open browser with keywords
        """
        try :
            keyword=keyword.split()
            keyword='+'.join(keyword)
            url = "https://www.google.co.in/search?q=" + keyword + "&source=lnms&tbm=isch"
            self.browser.get(url)
        except Exception as e:
            logger_obj.log_print('Scrapper.py(createURL) has exception ' +str(e),'exception')

    def scroll_to_end(self):
        """
        this function scrolls browser to end of the window size
        :return:
        """
        try:
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(2)
        except Exception as e:
            logger_obj.log_print('Scrapper.py(scroll_to_end) has exception' +str(e),'exception')

    def close_browser(self):
        """
        This function closes the browser
        :return:
        """
        try:
            self.browser.close()
        except Exception as e:
            logger_obj.log_print('Scrapper.py(close_browser) has exception'+str(e),'exception')

    def save_url(self,thumbnail_image,current_count,no_thumbnail_images,final_images,req_id,email,cassandra):
        """
        This function store url of images to database and return set of the url
        :param thumbnail_image:Thumbnails selected
        :param current_count:current count of url found
        :param no_thumbnail_images:Number of images selected
        :param final_images:Images URL found
        :param req_id:Unique Request id
        :param email:Email id of user
        :param cassandra:Cassandra object
        :return: set of url found
        """
        try:
            task_end = False
            for img in thumbnail_image[current_count:no_thumbnail_images]:
                try:
                    img.click()
                    time.sleep(1)
                except Exception as e:
                    logger_obj.log_print('Scrapper.py - Save_url has ecxception'+str(e),'exception')
                    continue

                opened_image = self.browser.find_element_by_css_selector('img.n3VNCb')
                for actual_image in opened_image:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        if not actual_image.get_attribute('src') in final_images:
                            final_images.add(actual_image.get_attribute('src'))
                            cassandra.insert_url(req_id, email, actual_image.get_attribute('src'))
                            current_count=current_count+1

                if current_count >= self.count_image:
                    task_end = True
                    break
            return final_images, current_count, task_end
        except Exception as e:
            logger_obj.log_print('Scrapper - store_url has exception'+str(e), 'exception')

    def fetch_thumbnails(self,req_id,email,cassandra):
        """
        It fetched thumnail of images
        :param req_id:Unique_id of request
        :param email:email id given by user
        :param cassandra:Cassandra object
        :return:
        """
        try:
            final_images = set()
            current_count=0
            task_finished = False

            while current_count<self.count_image and not task_finished:
                self.scroll_to_end()

                if self.browser.find_element_by_css_selector('.mye4qd'):
                    self.browser.execute_script('document.querySelector(".mye4qd").click()')

                thumbnail_image =self.browser.find_element_by_css_selector('img.Q4LuWd')
                no_thumbnail_image = len(thumbnail_image)
                final_images, current_count, task_finished = self.save_url(thumbnail_image, current_count, no_thumbnail_image, final_images, req_id, email, cassandra)
            logger_obj.log_print('Image url has been downloaded ','info')

            self.close_browser()
        except Exception as e:
            logger_obj.log_print('Scrapper.py - fetch_thumbnails has exception'+str(e), 'exception')




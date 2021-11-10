import datetime
from dateutil import tz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from Helper import HelperClass

from Logger import Logging

logger_obj = Logging("Advance Image Downloader")
logger_obj.initialize_logger()

jobstores = {
}
executors = {
    'default': ThreadPoolExecutor(20),
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
ap_scheduler = BackgroundScheduler(jobstores=jobstores,executors = executors, job_defaults=job_defaults, timezone='Asia/Kolkata')

ap_scheduler.start()

class ScheduleJob:
    global ap_scheduler

    def __init__(self):
        """
        Initialize scheduler object
        ap_scheduler: ap_scheduler object
        """
        try:
            self.scheduler = ap_scheduler
        except Exception as e:
            logger_obj.log_print('Scheduler.py has exception', 'Exception')
            raise Exception(e)

    def insert_request(self,keyword,date, time, count_image, email, req_id):
        """
        Function add current request into queue for processing
        :param keyword: Input given by user for image scrapping
        :param date:Date at which job should run
        :param time: time at which job should run
        :param count_image:No of images user want
        :param email:email of the user
        :param req_id:Unique id of the request
        """
        try:
            date_list = date.split('-')
            time_list = time.split(':')
            year, month, day = date_list[0], date_list[1], date_list[2]
            hour, minute = time_list[0], time_list[1]

            date_inserted = datetime.datetime(day=int(day), month=int(month), year=int(year), hour=int(hour),
                                              minute=int(minute), tzinfo=tz.gettz('Asia/Kolkata'))

            current_date = datetime.datetime.now(tz.gettz('Asia/Kolkata'))
            print('current date is {} and input date is {}'.format(current_date, date_inserted))

            if current_date < date_inserted:
                helper = HelperClass()

                self.scheduler.add_job(helper.helper_image,'cron',[keyword, count_image, email, req_id, ScheduleJob()], day=day, month=month,year=year,
                                       hour=hour,minute=minute,id=str(req_id))

            else:
                logger_obj.log_print('Scheduler.py has exception. Please enter present or forward date', 'Exception')
                raise Exception('Please enter present or forward date')
        except Exception as e:
            logger_obj.log_print('Scheduler.py has exception.','Exception')
            raise Exception ('need to check inputs')

    def delete_files_job_queue(self, req_id, time_to_delete):
        """
        This function deletes folder,zip file created to handle the request
        :param req_id: Unique Req_id of user
        :param time_to_delete: time adter which files gets deleted
        """
        try:
             current_date = datetime.datetime.now(tz.gettz('Asia/Kolkata'))
             delete_time = current_date + datetime.timedelta(minutes=time_to_delete)

             self.scheduler.add_job(HelperClass.helper_delete, 'cron', [req_id], day = delete_time.day, month= delete_time.month, year=delete_time.year,
                                    hour = delete_time.hour, minute=delete_time.minute, id=str(req_id))

        except Exception as e:
            logger_obj.log_print('Scheduler.py - delete_files_job_queue has exception', 'Exception')
            raise Exception(e)


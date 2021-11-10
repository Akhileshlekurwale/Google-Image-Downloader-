import re
import uuid
from flask import Flask,render_template,request,send_file
from flask_cors import cross_origin
from Logger import Logging
from Scheduler import ScheduleJob

logger_obj = Logging("Advance Image Downloader")
logger_obj.initialize_logger()

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
@cross_origin()
def index():
    """
    It shows index page
    """
    try:
        if request.method =='GET':
            logger_obj.log_print('Index Function','info')
            logger_obj.log_print('rendering Index page','Info')
            return render_template('Index.html')
        else:
            logger_obj.log_print('App.py has thrown exception','Exception')
            return render_template('Error.html',msg='Method restricted')
    except Exception as e:
        logger_obj.log_print('App.py has thrown Exception'+str(e), 'Exception')
        return render_template('Error.html')

@app.route('/job_submitted', methods = ['GET','POST'])
@cross_origin()
def Job_submitted():
    """
    This function perform all action after user inputs all details
    """
    try:
        if request.method == 'POST':
            logger_obj.log_print('In Job_submitted function', 'info')
            keyword = request.form['keyword'].lower()
            date = request.form['date']
            time = request.form['time']
            email = request.form['email']
            count_image = request.form['images']

            is_valid, error = validate_inputs(keyword,date, time, email, count_image)

            if is_valid:
                req_id = uuid.uuid4() # creating unique id for req

                schedule_job = ScheduleJob() #creating object of Schedulejob class

                schedule_job.insert_request(keyword, date, time, int(count_image),email, req_id)

                logger_obj.log_print('Job is added in queue','info')

                return render_template('Job_Submitted.html')
            else:
                return render_template('Error.html',msg='error')

        else:
            logger_obj.log_print('App.py has thrown exception ', 'Exception')
            return render_template('Error.html', msg = 'Method not allowed')

    except Exception as e:
        logger_obj.log_print('App.py has thrown exception','Exception')
        return  render_template('Error.html',msg=str(e))

@app.route('/download/<search_term>/<uuid:req_id>', methods= ['GET','POST'])
@cross_origin()
def download(search_term,req_id):
    """
    Sends zipfile to user
    :param search_term: Search query for user
    :param req_id:Unique req_id of user
    """
    try:
        logger_obj.log_print('Inside the download route','info')
        str_req_id = str(req_id)

        return send_file(str_req_id + '_zipfile.zip', as_attachment=True,attachment_filename=search_term +'.zip')

    except Exception as e:
        logger_obj.log_print('App.py has exception'+str(e),'Exception')
        return render_template('error.html',msg='Link expired')

def validate_inputs(keyword,date,time,email,count_image):
    """
    validate the input given by user
    :param keyword: search keyword given  by user
    :param date:date for scheduling job
    :param time: time for scheduling job
    :param email: email input given by user
    :param count_image: total number of images requested by user
    :return:Boolean if it is validate or not
    """
    try :
        if keyword != '' and date !='' and time !='' and email !='' and count_image !='':
            count_image = int(count_image)
            if 1 < count_image < 500:
                if re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                    return True, None
                else:
                    logger_obj.log_print("Email address is not correct", 'Exception')

                    return False, 'Invalid email address'

            else:
                logger_obj.log_print('Number of images should be below 500','Exception')
                return  False, 'No of images should be below 500'

        else:
            logger_obj.log_print('Please input all fields','exception')
            return False ,'Please input al fields'

    except Exception as e:
        raise Exception(e)



if __name__ =='__main__':
    app.debug = True
    app.run()






#####################################################################################
__author__='acgreyjo'
#
#  1. File is a stand alone file that
#     will read file for any new items
#  2. will
# Documentation: https://schedule.readthedocs.io/en/stable/examples.html#cancel-a-job
#####################################################################################
import subprocess
import schedule
import time
import six
import os
#
# def create_a_function(*args, **kwargs):
#
#     def function_template(*args, **kwargs):
#         pass
#
#     return function_template
#
# my_new_function = create_a_function()

scheduler_controller_pending = r'application/pending_schedule.txt'
scheduler_controller_canceling = 'application/cancel_schedule.txt'


class Controller():

    def __init__(self):
        self.jobs_running = {}      # holds all jobs actively running

    def job(self, fld_name):
        '''
            Uses folder name to determine
            file path and execute the proper configuration
        '''
        print(f'Working..{fld_name}')
        py_exe = r'C:\Python27\python.exe ' if six.PY2 else r'C:\Python37\python.exe '
        config = f'application//ScheduledOutput//{fld_name}//setup_configuration.py'
        result = subprocess.call([py_exe, 'application/analyzer.py', '-setup', config])

    def set_interval(self, fld_name, number):
        '''
            sets jobs interval schedules
        '''
        if not (':' in str(number)):
            job = schedule.every(int(number)).seconds.do(self.job, fld_name)
        else:
            print('Before setting...')
            job = schedule.every().day.at(str(number)).do(self.job, fld_name)
            print('setting interval..')
        # schedule.every(10).seconds.do(job)
        # schedule.every(10).minutes.do(job)
        # schedule.every().hour.do(job)
        # schedule.every().day.at("10:30").do(job)
        # schedule.every().monday.do(job)
        # schedule.every().wednesday.at("13:15").do(job)
        # schedule.every().minute.at(":17").do(job)
        self.jobs_running[fld_name] = job
        print('Job added.')

    def process_schedule_pending(self, fname=''):
        '''
            Reads in scheduling details from input
            file format: <folder_name>,<2021-06-16T18:51>\n
                         <folder_name>,<2021-06-16T18:51>\n
        '''
        with open(fname,'r') as fhdl:
            content = fhdl.readlines()
        for item in content:
            fld_name,date_time = item.rstrip().split(',')
            date_str,time_interval = date_time.split('T')
            print(f'folderName:{fld_name} date_str:{date_str} time_interval:{time_interval}')
            yield fld_name, time_interval
        # erase the content of the file, following adding all items to scheduler
        open(fname, "w").close()

    def process_schedule_canceling(self, fname=''):
        '''
            function uses folder name as key to
            get job object and cancel from schd.
            format: <folder_name>\n
                    <folder_name>\n
        '''
        with open(fname,'r') as fhdl:
            content = fhdl.readlines()
        for item in content:
            fld_name = item.rstrip()
            job_obj = self.jobs_running[fld_name]
            schedule.cancel_job(job_obj)
        # erase the content
        open(fname, "w").close()

    def do_job(self, name):
        print(f'Working...{name}')


def process(ctrl_schedule):
    '''
        handles reading pending_schedule.txt
        & cancel_schedule.txt to control the
        scheduling processes
    '''
    if os.stat(scheduler_controller_pending).st_size > 0:
        # add new items to scheduler when file size > 0
        for (name,interval) in ctrl_schedule.process_schedule_pending(fname=scheduler_controller_pending):
            print(f'name: {name} => interval: {interval}')
            ctrl_schedule.set_interval(name, 10)#interval) #10     #todo change interval to input interval
    if os.stat(scheduler_controller_canceling).st_size > 0:
        # cancel items from scheduler when file size > 0
        ctrl_schedule.process_schedule_canceling(fname=scheduler_controller_canceling)


if __name__ == '__main__':
    ctrl_obj = Controller()
    while True:
        schedule.run_pending()
        print('.')
        try:
            process(ctrl_obj)
        except:
           print('Error With Scheduler')
        time.sleep(1)

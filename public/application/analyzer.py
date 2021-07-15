################################################################
__author__='acgreyjo'
#
#
#
################################################################
import os
import sys
import importlib
import argparse
import pandas as pd
import io
import requests
from datetime import datetime
sys.path.append(r'../../application')
from processor import *

class Analyzer(object):
    def __init__(self, setup_config='', proxy=''):
        self.config_file = setup_config
        self.proxy = proxy
        self.task_name = ''
        self.dFrame = None
        self.url_to_data = ''
        self.output_file_path = ''
        self.program_name = ''
        self.groupby_column = []
        self.ignore_column = []
        self.treatment_column = []
        self.x_column = []
        self.y_column = []
        self.dist_types = []
        self.input_validate()
        self.results = {}

    def input_validate(self):
        '''
            Function validates user input found in the configuration
            file that is passed in. Ensure that default class variables
            are present
        :return: None
        '''
        setup_mod_obj = None
        if self.config_file:
            abs_path = os.path.abspath(self.config_file)
            print('[-i-] Current Path:', abs_path)
            spec = importlib.util.spec_from_file_location(abs_path, abs_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            setup_mod_obj = module

        assert hasattr(setup_mod_obj, 'url_to_data')
        assert hasattr(setup_mod_obj, 'task_name')
        assert hasattr(setup_mod_obj, 'output_file_path')
        assert hasattr(setup_mod_obj, 'hdf5_file_name')
        assert hasattr(setup_mod_obj, 'column_groupby')
        assert hasattr(setup_mod_obj, 'program_name')
        assert hasattr(setup_mod_obj, 'ignore_columns')
        assert hasattr(setup_mod_obj, 'treatment_column')
        assert hasattr(setup_mod_obj, 'x_column')
        assert hasattr(setup_mod_obj, 'y_column')
        assert hasattr(setup_mod_obj, 'dist_type')

        self.url_to_data = setup_mod_obj.url_to_data
        self.task_name = setup_mod_obj.task_name
        self.output_file_path = setup_mod_obj.output_file_path
        self.groupby_column = setup_mod_obj.column_groupby
        self.program_name = setup_mod_obj.program_name
        self.ignore_column = setup_mod_obj.ignore_columns
        self.treatment_column = setup_mod_obj.treatment_column
        self.x_column = setup_mod_obj.x_column
        self.y_column = setup_mod_obj.y_column
        self.dist_types = setup_mod_obj.dist_type
        print('[-i-] Config Validation Completed.')

    def load_data(self):
        '''
        This dataset contains 21 body dimension measurements as well as age,
        weight, height, and gender on 507 individuals. The 247 men and 260
        women were primarily individuals in their twenties and thirties, with a
        scattering of older men and women, all exercising several hours a week.

        SOURCE:
            Measurements were initially taken by the first two authors - Grete
            Heinz and Louis J. Peterson - at San Jose State University and at the
            U.S. Naval Postgraduate School in Monterey, California. Later,
            measurements were taken at dozens of California health and fitness
            clubs by technicians under the supervision of one of these authors.
        :return: dataFrame
        '''
        headers = ['Biacromial diameter', 'Biiliac diameter', 'Bitrochanteric', 'Chest depth', 'Chest diameter',
                  'Elbow diameter', 'Wrist diameter', 'Knee diameter', 'Ankle diameter', 'Shoulder girth', 'Chest girth',
                  'Waist girth', 'Navel girth', 'Hip girth', 'Thigh girth', 'Bicep girth', 'Forearm girth', 'Knee girth',
                  'Calf maximum girth', 'Ankle minimum girth', 'Wrist minimum girth', 'Age', 'Weight', 'Height', 'Gender'
                   ]

        try:
            _df = pd.read_csv(self.url_to_data, delim_whitespace=True)
        except Exception as e:
            print('[-w-] Using proxy.....')
            stream = requests.get(self.url_to_data, proxies={'http': self.proxy}).text
            _df = pd.read_csv(io.StringIO(stream), delim_whitespace=True)
        # set header and replace gender column to categorical
        _df.columns = headers
        _df['Gender'] = _df['Gender'].apply(lambda x: 'M' if x == 1 else 'F')
        self.dFrame = _df
        print('[-i-] DataFrame:\n', self.dFrame.head())
        # self.write_data(r'data\inputdata.csv')

    def write_data(self, file_path=''):
        '''
            writes dataframe data to local store
        :param file_path: internal file location
        :return: None
        '''
        if not self.dFrame.empty:
            self.dFrame.to_csv(file_path, index=False)

    def process_data(self):
        '''
            process and plot base on distribution
        :return:
        '''

        for plot_type in self.dist_types:
            print(f'[-i-] Running Plot type: {plot_type}')
            if plot_type.lower() == 'dist':
                print('Processing for dist.')
                # from analytika.application.dist import Dist
                from dist import Dist
                dist_obj = Dist()
            elif plot_type.lower() == 'dist_by':
                print('Processing for distby')
                from dist_by import Dist_By
                dist_obj = Dist_By()
            elif plot_type.lower() == 'hist_2d':
                print('Processings for Hist2D')
                from hist_2d import Hist_2D
                dist_obj = Hist_2D()
            elif plot_type.lower() == 'var':
                print('Processing for variability')

            dist_obj.dFrame = self.dFrame
            dist_obj.task_name = self.task_name
            dist_obj.x_columns = self.x_column
            dist_obj.y_columns = self.y_column
            dist_obj.groupby = self.groupby_column
            if dist_obj:
                dist_obj.visualize()
                self.results[plot_type] = dist_obj.results

    def create_folder(self, use_folder=''):
        '''
            with current setting os.getcwd() should be equal to public
            folder /analytika/public
        :param use_folder:
        :return:
        '''
        if not use_folder:
            # create default task folders without datetime stamps
            # use_folder = os.path.join(os.getcwd(),'..','application','scheduledOutput',self.task_name)
            use_folder = os.path.join(os.getcwd(),'application','scheduledOutput',self.task_name)
        print(use_folder)
        if not os.path.exists(use_folder):
            os.makedirs(use_folder)

    def generate_report(self):
        # generate datetime and use as sub-folder
        date = datetime.now()
        cur_date = date.strftime("%Y-%m-%d_%H-%M-%S")

        tmp_str = ''
        for idx,dist_type in enumerate(self.dist_types):
            print(f'[-i-] Generate Report:{dist_type}')
            tmp_str += '''
                <div class="card_stack">
                    <h1>Card {}</h1>
                    {}
                </div>
            '''.format(str(idx), self.results[dist_type].output_plots[0])
        template = '''
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="UTF-8" />
                        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                        <meta http-equiv="X-UA-Compatible" content="ie=edge" />
                        <title></title>
                        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/css/bootstrap.min.css" />
                        <link rel="stylesheet" href="../../../../css/index.css" />
                    </head>
                    <body>
                        <main>
                            {}
                        </main>
                    </body>
                </html>
        '''.format(tmp_str)
        # write out report
        # use_folder = os.path.join(os.getcwd(), '..', 'application', 'scheduledOutput', self.task_name, cur_date)
        use_folder = os.path.join(os.getcwd(),'application', 'scheduledOutput', self.task_name, cur_date)
        self.create_folder(use_folder=use_folder)
        file_path = os.path.join(use_folder, 'report.html')
        with open(file_path,'w') as hdl:
            hdl.write(template)


def parse_options():
    #   parse the command line input
    parser = argparse.ArgumentParser()
    parser.add_argument('-setup', required=True, action='store')
    parser.add_argument('-proxy', required=False, action='store')
    parser.add_argument('-debug', required=False, action='store_true')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    print('[-i-] Analyzer Starting...')
    options = parse_options()
    config_file = options.setup
    use_proxy = options.proxy
    run_analyzer = Analyzer(setup_config=config_file, proxy=use_proxy)
    run_analyzer.create_folder()
    run_analyzer.load_data()
    run_analyzer.process_data()
    run_analyzer.generate_report()
    print('[-i-] Task Completed.')
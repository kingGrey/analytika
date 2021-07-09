################################################################
__author__='acgreyjo'
#
#
#
################################################################
import os
import importlib
import argparse
import pandas as pd
import io
import requests
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
        self.write_data(r'data\inputdata.csv')

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
        proc_hdl = PlotterBase()
        proc_hdl.dFrame = self.dFrame
        proc_hdl.task_name = self.task_name
        proc_hdl.x_columns = self.x_column
        proc_hdl.y_columns = self.y_column
        proc_hdl.groupby = self.groupby_column
        proc_hdl.dist_type = self.dist_types
        if proc_hdl:
            proc_hdl.runner()


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
    run_analyzer.load_data()
    run_analyzer.process_data()
    print('[-i-] Task Completed.')
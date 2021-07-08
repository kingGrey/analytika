import os
import importlib
import argparse


class Analyzer(object):
    def __init__(self, setup_config=''):
        self.config_file = setup_config
        self.df = None
        self.file = ''
        self.url_to_data = ''
        self.output_file_path = ''
        self.program_name = ''
        self.groupby_column = []
        self.ignore_column = []
        self.treatment_column = []
        self.x_column = []
        self.y_column = []
        self.input_validate()

    def input_validate(self):
        '''

        :return:
        '''
        setup_mod_obj = None
        if self.config_file:
            abs_path = os.path.abspath(self.config_file)
            print('[-i-] Current Path:', abs_path)
            spec = importlib.util.spec_from_file_location(abs_path, abs_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            setup_mod_obj = module

        assert hasattr(setup_mod_obj, 'input_data_file')
        assert hasattr(setup_mod_obj, 'url_to_data')
        assert hasattr(setup_mod_obj, 'output_file_path')
        assert hasattr(setup_mod_obj, 'hdf5_file_name')
        assert hasattr(setup_mod_obj, 'column_groupby')
        assert hasattr(setup_mod_obj, 'program_name')
        assert hasattr(setup_mod_obj, 'ignore_columns')
        assert hasattr(setup_mod_obj, 'treatment_column')
        assert hasattr(setup_mod_obj, 'x_column')
        assert hasattr(setup_mod_obj, 'y_column')

        self.file = setup_mod_obj.input_data_file
        self.url_to_data = setup_mod_obj.url_to_data
        self.output_file_path = setup_mod_obj.output_file_path
        self.groupby_column = setup_mod_obj.column_groupby
        self.program_name = setup_mod_obj.program_name
        self.ignore_column = setup_mod_obj.ignore_columns
        self.treatment_column = setup_mod_obj.treatment_column
        self.x_column = setup_mod_obj.x_column
        self.y_column = setup_mod_obj.y_column
        print('[-i-] Config Validation Completed.')


def parse_options():
    #   parse the command line input
    parser = argparse.ArgumentParser()
    parser.add_argument('-setup', required=True, action='store')
    parser.add_argument('-debug', required=False, action='store_true')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    print('[-i-] Analyzer Starting...')
    options = parse_options()
    config_file = options.setup
    run_analyzer = Analyzer(setup_config=config_file)
    with open(r'c:\Temp\writeme.txt','w') as f:
        f.write('Things fall apart')

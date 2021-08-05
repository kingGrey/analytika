################################################
__author__='acgreyjo'
#
#   Class aims to test some of the basic simpler
#   features/properties of this application that
#   are deemed testable.
################################################
import os
import pandas as pd
import unittest
from analytika.public.application.analyzer import Analyzer


class AnalytikaTestCase(unittest.TestCase):
    def setUp(self):
        '''
            setup - testing framework will automatically
            call it for each test implemented. Preps the
            required class variables
        :return:
        '''
        self.analyzer = Analyzer(setup_config='../setup_configuration.py')

    def test_validate_config(self):
        '''
            testing validates user configuration file
            and initializing class variables
        :return:
        '''
        # self.assertTrue(self.analyzer.input_validate())
        pass

    def test_loadable_data(self):
        '''
            testing that url provided in configuration file
            is loadable
        :return: dataFrame.shape > 0
        '''
        try:
            _df = pd.read_csv(self.analyzer.url_to_data, delim_whitespace=True)
        except Exception as e:
            raise
        self.assertIsNotNone(_df)

    def test_schedule_collateral(self):
        '''
            test pending and cancel input
            monitoring files
        :return: bool
        '''
        files = ['monitor/cancel_schedule.txt', 'monitor/pending_schedule.txt']
        for file in files:
            file = os.path.join('..', file)
            self.assertTrue(os.path.exists(file),True)

    def test_something(self):
        self.assertEqual(True, True)

    def tearDown(self):
        '''
            handles test clean up steps
        :return: None
        '''
        self.analyzer = None


if __name__ == '__main__':
    unittest.main()

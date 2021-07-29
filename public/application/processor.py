#################################################
__author__='acgreyjo'
#
# This file acts as a base file for which other
# class inherit from. It defines the input details
# require for the processing collected from the
# user configuration file
##################################################
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as pltly
import pandas as pd
# from analytika.application.dot_dict import Dotdict
from dot_dict import Dotdict


class PlotterBase(object):
    def __init__(self):
        self.dFrame = None
        self.task_name = ''
        self.x_columns = []
        self.y_columns = []
        self.groupby = []
        self.results = Dotdict(dict(output_plots=[], plot_types=[], columns=[], index=[], plot_dframe=pd.DataFrame()))

    def visualize(self):
        '''
            handles plot generations
        :return:
        '''
        print('[-i-] Executing runner...')

    def generate_results(self, div_content,plot_type):
        '''
            handles processing and plot information stored
            to dictionary
        :param div_content: card item to be add to report
        :param plot_type: plot type used
        :return: None
        '''
        self.results.output_plots.append(div_content)
        self.results.plot_types.append(plot_type)


if __name__ == '__main__':
    print('[-i-]Processor is Running.....')
#################################################
__author__='acgreyjo'
#
#
#
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
        print('[-i-] Executing runner...')

    def generate_results(self, div_content,plot_type):
        self.results.output_plots.append(div_content)
        self.results.plot_types.append(plot_type)


if __name__ == '__main__':
    print('[-i-]Processor is Running.....')
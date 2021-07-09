#################################################
__author__='acgreyjo'
#
#
#
##################################################
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as pltly


class PlotterBase(object):
    def __init__(self):
        self.dFrame = None
        self.task_name = ''
        self.x_columns = []
        self.y_columns = []
        self.groupby = []
        self.dist_type = []

    def runner(self):
        print('[-i-] Executing runner...')
        for plot_type in self.dist_type:
            print(f'[-i-] Running Plot type: {plot_type}')
            if plot_type.lower() == 'dist':
                print('Processing for dist.')
                from analytika.application.dist import Dist
                dist_obj = Dist()
                dist_obj.visualize(self.dFrame)
            elif plot_type.lower() == 'dist_by':
                print('Processing for distby')
            elif plot_type.lower() == 'var':
                print('Processing for variability')





if __name__ == '__main__':
    print('[-i-]Processor is Running.....')
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

    def visualize(self):
        print('[-i-] Executing runner...')


if __name__ == '__main__':
    print('[-i-]Processor is Running.....')
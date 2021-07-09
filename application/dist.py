from analytika.application.processor import *
import plotly.express as px


class Dist(PlotterBase):
    def __init__(self):
        print('[-i-] Processing {}...'.format(self.__class__.__name__))
        super(Dist, self).__init__()

    def visualize(self):
        print('[-i-] Executing visualize...')
        print(self.dFrame.shape)
        print(f'taskname: {self.task_name}')

from.processor import *
import plotly.express as px


class Dist(PlotterBase):
    def __init__(self):
        print('[-i-] Processing {}...'.format(self.__class__.__name__))

    def visualize(self, dataFrame):
        print('[-i-] Executing visualize...')
        print(dataFrame.shape)

##############################################
__author__='acgreyjo'
#
#   This implementation generate a histogram
#   plot(s) based on data provided
##############################################

from processor import *
from plotly.subplots import make_subplots
from plotly.offline import plot
import math
import plotly.express as px
import plotly.graph_objs as go


class Hist_2D(PlotterBase):
    def __init__(self):
        print('[-i-] Processing {}...'.format(self.__class__.__name__))
        super(Hist_2D, self).__init__()

    def visualize(self):
        print('[-i-] Executing visualize...')
        print(self.dFrame.shape)
        print(f'taskname: {self.task_name}')
        num_subplot_per_row = 3
        cols = num_subplot_per_row
        rows = math.ceil((len(self.x_columns) * len(self.y_columns)) / num_subplot_per_row)
        fig = make_subplots(rows=rows, cols=cols, print_grid=True,horizontal_spacing=0.15, shared_yaxes=True)
        cur_row = 1
        cur_col = 1
        print('====Columns======',self.x_columns)
        for y_col_item in self.y_columns:
            for x_col_item in self.x_columns:
                fig.append_trace(go.Histogram2d(x=self.dFrame[x_col_item], y=self.dFrame[y_col_item],name=x_col_item.upper()),row=cur_row,col=cur_col)
                fig.update_xaxes(title_text=x_col_item.upper(), row=cur_row, col=cur_col)
                fig.update_yaxes(title_text=y_col_item.upper(), row=cur_row, col=cur_col)
                if cur_col == cols:
                    cur_row += 1
                else:
                    cur_col += 1
        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            title_text='DistBy',
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="yellow"
            )
        )
        # plot(fig)
        div = plot(fig, auto_open=False, show_link=False, output_type='div',config={'responsive':True})
        self.generate_results(div, self.__class__.__name__)


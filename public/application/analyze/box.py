# from analytika.application.processor import *
from processor import *
from plotly.subplots import make_subplots
from plotly.offline import plot
import math
import plotly.express as px
import plotly.graph_objs as go


class Box(PlotterBase):
    def __init__(self):
        print('[-i-] Processing {}...'.format(self.__class__.__name__))
        super(Box, self).__init__()

    def visualize(self):
        print('[-i-] Executing visualize...')
        print(self.dFrame.shape)
        print(f'taskname: {self.task_name}')
        grp_default_len = 0

        num_subplot_per_row = 3
        cols = num_subplot_per_row
        rows = math.ceil((len(self.x_columns) * len(self.y_columns)) / num_subplot_per_row)

        if self.groupby:
            grp_col = self.groupby[0]
            grp_by_unique_lst = self.dFrame[grp_col].unique()
            grp_default_len = len(grp_by_unique_lst)
            rows = math.ceil(rows*grp_default_len)

        fig = make_subplots(rows=rows, cols=cols, print_grid=True,horizontal_spacing=0.15, shared_yaxes=True)
        cur_row = 1
        cur_col = 1
        print('====Columns======', self.x_columns)
        print('=====Groupby=====', self.groupby)

        if grp_default_len > 0:
            for idx, grp_by_item in enumerate(grp_by_unique_lst):
                df_ = self.dFrame[self.dFrame[grp_col] == grp_by_item]
                for x_col_item in self.x_columns:
                    fig.append_trace(go.Box(x=df_[x_col_item],name=x_col_item.upper()),row=cur_row,col=cur_col)
                    fig.update_xaxes(title_text=grp_by_item.upper(), row=cur_row, col=cur_col)
                    # fig.update_yaxes(title_text='Count', row=cur_row, col=cur_col)

                    if cur_col == cols:
                        cur_row += 1
                        cur_col = 1
                    else:
                        cur_col += 1
        else:
            for x_col_item in self.x_columns:
                fig.append_trace(go.Box(y=self.dFrame[x_col_item], name=x_col_item.upper(),notched=True), row=cur_row, col=cur_col)
                # fig.update_xaxes(title_text=x_col_item.upper(), row=cur_row, col=cur_col)
                fig.update_yaxes(title_text='Count', row=cur_row, col=cur_col)

                if cur_col == cols:
                    cur_row += 1
                    cur_col = 1
                else:
                    cur_col += 1

        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            # height=400,
            # width=850,
            title_text='Box',
            # title_font_size=14,
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="yellow"
            )
        )
        # fig.show()
        # plot(fig)
        div = plot(fig, auto_open=False, show_link=False, output_type='div',config={'responsive':True})
        self.generate_results(div, self.__class__.__name__)


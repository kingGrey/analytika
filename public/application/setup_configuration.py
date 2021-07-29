#############################################################################
# Configuration file setup for incoming data analysis
#
# User Should be able to use data from a source and given that
# data pre-processing code is added, this configuration should
# serve to provide a summary of plots based on user setup
#
# Current column data-set definitions can be found here:
#   http://jse.amstat.org/datasets/body.txt
#
# current plot options : dist, dist_by, variability, bivariate, hist2d, box
###########################################################################

'''unique identifier'''
task_name = 'sched04'

'''url data source'''
url_to_data = 'http://jse.amstat.org/datasets/body.dat.txt'

'''categorical column not to be processed'''
ignore_columns = []

'''x column'''
x_column = ['Weight', 'Height', 'Age']

'''y column'''
y_column = ['Biacromial diameter']

'''column(s) names to group by'''
column_groupby = [] #['Gender']

'''result output path'''
output_file_path = r'c:\Temp'

'''filestore name'''
hdf5_file_name = 'mean_analysis_store'

'''id name'''
program_name = 'PGM1'

'''seperabale column identification'''
treatment_column = []

'''disribution type'''
dist_type =['box','dist','dist_by']        # dist, dist_by, variability, bivariate, hist2d, box

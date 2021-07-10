'''unique identifier'''
task_name = 'test_name'
'''url data source'''
url_to_data = 'http://jse.amstat.org/datasets/body.dat.txt'
'''categorical column not to be processed'''
ignore_columns = []
'''x column'''
x_column = ['Weight','Height','Age']
'''y column'''
y_column = ['Biacromial diameter']
'''column(s) names to group by'''
column_groupby = ['Gender']
'''result output path'''
output_file_path = r'c:\Temp'
'''filestore name'''
hdf5_file_name = 'mean_analysis_store'
'''id name'''
program_name = 'PGM1'
'''seperabale column identification'''
treatment_column = []
'''disribution type'''
dist_type = ['dist','dist_by']        # dist, disby, variability,

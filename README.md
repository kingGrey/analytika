# `Analytika`  
#### analyze input data and display data summaries
`Asante Grey-Johnson 2021`

This repository contains a program that takes user configuration in the format of
a `.py [python]` module file. With this file and a provided data set, the application then performs an ad-hoc run to summerizes and present some general plot types that best explains or gives the user more insights into the data being analyzed. 


 ## Roadmap stages
 This section shows the various phase items that is/are being worked on towards the completion of the project
 ##### Milestone 1..........     `[4 days]`
 - [x] Front-end implementation
 - [x] Configuration file implementation
 - [x] Handle data pull from source
 ##### Milestone 2..........     `[2.5 weeks]`
 - [x] Pre-processing and 
 - [x] Post-process of data based on user configuration file.
 ##### Milestone 3..........     `[2.5 weeks]`
 - [x] Add ad-hoc option
 - [x] Add scheduling option
 - [x] Generate reports      
 - [x] Add report link to front-end application
 - [x] Add Documentation
 - [ ] Testing
 

## Future stages
I expect that for future work, additional features that could be added are:
- [ ] Add user login options
- [ ] Add a fully functional database to store metadata for additional analysis
- [ ] Add time series plots to detect process shifts
- [ ] Add capability for data outlier detection
- [ ] Add capability for mean data analysis

## Build and Run
* `pip install -r requirements.txt`
#####  Scheduling
To enable scheduling - this is currently a standalone file run in the background that monitors `pending_schedule.txt` and `cancel_schedule.txt` once a task(s) have been scheduled from the main application
1. On a command line: start  `python` `scheduler.py`
##### Main run  
2. On another command line: `change directory` into project path `c:\<...>\analytika\public`
3. Launch: `node|nodemon jscripts\index.js`
4. From a browser launch application at `http://localhost:5000`

## Example
This configuration file contains the main settings the users would like the program to
analyze.

```python
'''unique identifier'''
task_name = 'task-name'

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
dist_type = ['dist_by','hist_2d']        # dist, dist_by, variability, bivariate, hist_2d, box
```
## Requirements
Tested with: 
* `python37`
* `nodejs`
* currently on `Windows platform`

## Acknowledgements
 

## License

This work is made available under the "MIT License". Please
see the file `LICENSE` in this distribution for license
terms.

# analytika - analyze input data and display data summeries
Asante Grey-Johnson 2021

This repository contains a program that takes user configuration in the format of
a .py [python] module file. With this file and a provided data set, the application then performs an ad-hoc run to summerizes and present some general plot types that best explains or gives the user more insights into the data being analyzed. 


 ## Roadmap stages
 This section shows the various phase items that is/are being worked on towards the completion of the project
 ##### Milestone 1..........     [1 day]
 - [ ] Front-end implementation
 - [x] Configuration file implementation
 - [ ] Handle data pull from source
 ##### Milestone 2..........     [2 weeks]
 - [ ] Pre and Post-process of data based on user configuration file.
 ##### Milestone 3..........     [1.5 weeks]
 - [ ] Generate Report      
 - [ ] Add report link to front-end application

## Future stages
I expect that for future work, additional features could be added to enable the application to run fully automated
- [ ] Add scheduling option
- [ ] Add user login options
- [ ] Add a fully functional database to store metadata for additional analysis
- [ ] Add time series plots to detect process shifts
- [ ] Add capability for data outlier detection
- [ ] Add capability for mean data analysis

## Build and Run
1. on command line launch: Nodemon index.js
2. From a browser launch application at http://localhost:5000

## Example
This configuration file contains the main settings the users would like the program to
analyze.

```python
from analytika.application import ..

```

## Acknowledgements


## License

This work is made available under the "MIT License". Please
see the file `LICENSE` in this distribution for license
terms.

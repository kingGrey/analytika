const http = require('http');
const fs = require('fs');
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload')
const io = require('socket.io')(http);
const app = express();
const port = process.env.PORT || 5000;
const report_dir = '../application/ScheduledOutput'
const host_name = `http://localhost:${port}`

//configure express
app.use(express.urlencoded({extended:true}));
app.use(express.static('../public'));

//Here we are configuring express to use body-parser as middle-ware.
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

//set max file-size for upload
app.use(fileUpload({
  limits: { fileSize: 50 * 1024 * 1024 },
}));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname,'../index.html'))
});

        /*#########################
                   AD_HOC
         ##########################*/

/**************************************
*  handles adhoc button click action
*  transfer from client side to execute
*  analysis on data
* @return - None
***************************************/
app.post('/adhoc_run_click', (req, res) => {
    console.log('Ad-Hoc Run clicked...');
    console.log(req.body.path);             // configuration path
    console.log(req.body.folder_name)       //date_time name

    //uses child_process.spawn of subprocess
    var spawn = require("child_process").spawn;
    var child = spawn('C:\\Python37\\python.exe',['application/analyzer.py','-setup',`${req.body.path}`]);
    app_rslt_str = ''

    // Takes stdout data from script which executed
    // with arguments and send this data to res object
    child.stdout.on('data', function(data) {
        app_rslt_str += data.toString()
        console.log('=========================\n',app_rslt_str)
    } )
    // on end return application msg to client
    child.stdout.on('end', function(data){
        res.send(JSON.stringify(app_rslt_str))
        console.log('=========================')
    })
    // Handle error output
    child.stderr.on('data', (data) => {
        // convert data to a readable string, print to console
        console.log(data.toString());
    });

    child.on('exit', (code) => {
        console.log("Process quit with code : " + code);
    });
});

/****************************************
* handles cancel button click
* @return -
*****************************************/
app.post('/adhoc_cncl_click', (req, res) =>{
    console.log('Ad-Hoc Cancel run...')
    console.log(req.body.path)
})

/****************************************
* handles adhoc configuration upload to
* be save on server
* @return -
*****************************************/
app.post('/save_config', (req, res) => {
    console.log('Saving config...')
    const fileName = req.files.myFile.name
    const path = 'c:/Temp/' + fileName
    const config_file = req.files.myFile
    console.log('File Received:',fileName)
    console.log('Server path:',path)


    config_file.mv(path, (error) => {
    if (error) {
      console.error(error)
      res.writeHead(500, {
        'Content-Type': 'application/json'
      })
      res.end(JSON.stringify({ status: 'error', message: error }))
      return
    }

    res.writeHead(200, {
      'Content-Type': 'application/json'
    })
    res.end(JSON.stringify({ status: 'success', path: path }))
    })
});

/************************************************
* handles configuraiton storage for scheduler
* from client to server
* @return -
**************************************************/
app.post('/save_config_schedule', (req, res) => {
    console.log('Saving config...')
    let config_file = req.files.config_file
    let fileName = config_file.name
    let fld_name = req.body.folder_name
    let path_ = path.join(__dirname, report_dir, fld_name, fileName)
    let rel_path = path.join(report_dir,fld_name,fileName)
    console.log('File Received:',fileName)
    console.log('Server path:',path_)

    config_file.mv(path_, (error) => {
    if (error) {
      console.error(error)
      res.writeHead(500, {
        'Content-Type': 'application/json'
      })
      res.end(JSON.stringify({ status: 'error', message: error }))
      return
    }
    res.writeHead(200, {
      'Content-Type': 'application/json'
    })
    res.end(JSON.stringify({ status: 'success', path: rel_path }))
    })
});


        /*##########################
                Scheduler
         ###########################*/

/******************************************
* helper function to enable file creation
* on the server
* @return - Status of creation
*******************************************/
app.post('/create_folder', (req, res) => {
    fld_name = req.body.folder_name
    folder_option = req.body.folder_option
    console.log(`Create New Folder ${fld_name}`)
    full_path = path.join(__dirname,report_dir, fld_name)
    console.log(full_path)
    console.log(req.body)
    try {
      if (folder_option == 'overwrite'){
        fs.rmdirSync(full_path)
      }
      if (!fs.existsSync(full_path)) {
        fs.mkdirSync(full_path)
        res.send({'status':'success'})
      }
      else{
        console.log('Folder Already Exists')
        res.send({'status':'exists'})
      }
    } catch (err) {
      console.error(err)
      res.send({'status':err})
    }
});

/***********************************************
* creates file to hold schedule run times and
* this is stored local file - run_interval.txt
* to be use for reload incase full system stopage
* @return - None
************************************************/
app.post('/create_interval_file',(req, res) => {
    fld_name = req.body.folder_name
    run_interval = req.body.task_interval
    console.log(fld_name +':' + run_interval)
    full_path = path.join(__dirname, report_dir, fld_name, 'run_interval.txt')
    console.log(full_path)
    try {
      const data = fs.writeFileSync(full_path, run_interval.toString())
      console.log('Written Successfully')
    } catch (err) {
      console.error(err)
    }
})

/************************************************
* handles writing <task-name>,<interval>  into
* pending_schedule.txt to be added to scheduler
* @return - Notification of addition
************************************************/
app.post('/schedule_run_click', (req, res) => {
    console.log('schedule run clicked..')
    console.log(req.body)
    full_path = path.join(__dirname,'../application/pending_schedule.txt')
    content = req.body.folder_name+','+ req.body.interval + '\n'
    if (fs.existsSync(full_path)){
        console.log('file exists, append.')
        fs.appendFileSync(full_path, content)
    }
    else{
        console.log('file not found. Create it.')
        try {
          const data = fs.writeFileSync(full_path, content)
          //file written successfully
          console.log('Written Successfully')
        } catch (err) {
          console.error(err)
        }
    }
    res.send(JSON.stringify('added'))
})


        /*#########################
                   REPORT
         ###########################*/

/********************************************
* handles generation of side bar treeview to
* display all task reports generated by either
* adhoc or scheduled process.
* @return - None
*********************************************/
app.get('/report_details',(req, res) =>{
    console.log('Information log...')

    defaultData = []
    var tmp_lst = []
    var files = fs.readdirSync(path.join(__dirname,report_dir))
    console.log(files)
    for(const fld of files){
        var lcl_dict = {}
        var nodes = []

        console.log('fld:',fld)
        lcl_dict['text'] = fld
        lcl_dict['href'] = '#href'
        lcl_dict['tags'] = ['Active']
        lcl_dict['nodes'] =[]
        var child_fld = path.join(__dirname,report_dir,fld)
        tmp_lst = []
        fs.readdirSync(child_fld).forEach(file => {
            var full_path = path.join(child_fld,file)        //get full path to folder
            console.log('fullpath:',full_path)
            if(fs.statSync(full_path).isDirectory()){
                // only for directories, skip __pycache__ folder generated
                if('__pycache__' != file){
                    var child_dict = {}
                    console.log('child files: '+file);
                    child_dict['text'] = file.toString()
                    child_dict['icon'] = "glyphicon glyphicon-stop"
                    child_dict['selectedIcon'] = "glyphicon glyphicon-stop"
                    //child_dict['href'] = '#href'
                    child_dict['nodes'] = []
                    lcl_dict['nodes'].push(child_dict)      // store child nodes

                    var grand_child = child_fld + '//'+ file
                    var grand_child_dict = {}
                    let dirCont = fs.readdirSync( grand_child );
                    var extension = 'html'
                    //search for .html file
                    let linker = dirCont.filter( file => file.match(new RegExp(`.*\.(${extension})`, 'ig')));
                    linker_name = linker[0]
                    grand_child_dict['text'] = linker_name
                    grand_child_dict['href'] = path.join('application','scheduledOutput',fld, file, linker_name)
                    child_dict['nodes'].push(grand_child_dict)      //store grand-child
                }
            }
        });
        defaultData.push(lcl_dict)
    }
    res.send({status:'Success', value:defaultData, folder:files})
});

//server enable
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});


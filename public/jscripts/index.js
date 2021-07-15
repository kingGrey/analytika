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

app.post('/adhoc_run_click', (req, res) => {
    console.log('Ad-Hoc Run clicked...');
    console.log(req.body.path);             // configuration path
    console.log(req.body.folder_name)       //date_time name

    // Use child_process.spawn method from
    // child_process module and assign it
    // to variable spawn
    var spawn = require("child_process").spawn;
    var child = spawn('C:\\Python37\\python.exe',['application/analyzer.py','-setup',`${req.body.path}`]);
    app_rslt_str = ''
//    process.stdout.pipe(child.stdout)

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

app.post('/adhoc_cncl_click', (req, res) =>{
    console.log('Ad-Hoc Cancel run...')
    console.log(req.body.path)
})

app.post('/save_config', (req, res) => {
    console.log('Saving config...')
    const fileName = req.files.myFile.name
    const path = 'c:/Temp/' + fileName //__dirname  + '/images/' + fileName
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

/*##########################
        Scheduler
 ###########################*/


/*#########################
           REPORT
 ###########################*/
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
                // only for directories
                var child_dict = {}
                console.log('child files: '+file);
                child_dict['text'] = file.toString()
                child_dict['icon'] = "glyphicon glyphicon-stop"
                child_dict['selectedIcon'] = "glyphicon glyphicon-stop"
    //          child_dict['href'] = '#href'
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
        });
        defaultData.push(lcl_dict)
    }
    res.send({status:'Success', value:defaultData, folder:files})
});

//server enable
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});


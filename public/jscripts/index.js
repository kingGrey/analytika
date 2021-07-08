const http = require('http');
const fs = require('fs');
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload')
const io = require('socket.io')(http);
const app = express();
const port = process.env.PORT || 5000;
const report_dir = 'ScheduledOutput'//'C:\\temp\\ScheduledOutput'
const host_name = `http://localhost:${port}`


app.use(express.urlencoded({extended:true}));
app.use(express.static('../public'));

//Here we are configuring express to use body-parser as middle-ware.
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(fileUpload({
  limits: { fileSize: 50 * 1024 * 1024 },
}));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname,'../index.html'))
});



//########## AD_HOC #############

app.post('/adhoc_run_click', (req, res) => {
    console.log('Ad-Hoc Run clicked...');
    console.log(req.body.path);

    // Use child_process.spawn method from
    // child_process module and assign it
    // to variable spawn
    var spawn = require("child_process").spawn;
    var child = spawn('C:\\Python37\\python.exe',['../application/analyzer.py','-setup',`${req.body.path}`]);
    app_rslt_str = ''
//    process.stdout.pipe(child.stdout)

    // Takes stdout data from script which executed
    // with arguments and send this data to res object
    child.stdout.on('data', function(data) {
        app_rslt_str += data.toString()
        console.log('...data...',app_rslt_str)
//        res.send(data.toString());
    } )
    child.stdout.on('end', function(data){
        res.send(JSON.stringify(app_rslt_str))
        console.log('done....sssssss')
    })
    // Handle error output
    child.stderr.on('data', (data) => {
        // As said before, convert the to a readable string.
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


app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});


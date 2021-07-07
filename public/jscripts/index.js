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


app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});


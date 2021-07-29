//element declarations
var date_control = document.querySelector('input[type="datetime-local"]');
var task_name = document.querySelector('#name')
var typing_timer;
var typing_complete_interval = 1000;            //1 sec

/*****************************************
* handles detection of the keyup action on
* scheduled page for task-name creation on
* the server side.
* @return - None
******************************************/
task_name.addEventListener('keyup', () =>{
    clearTimeout(typing_timer);
    if (task_name.value){
        typing_timer = setTimeout(validate_task_name,typing_complete_interval);
    }

})

/***********************************************
* handles creation task-name if does not exists
* else can overwrite file if user decides so
* @return - confirmation
***********************************************/
function validate_task_name(){
//  alert(task_name.value)
  const formData = new FormData()
  formData.append('folder_name', task_name.value)
  formData.append('folder_option','')
  fetch('/create_folder', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.status)
    status = data.status
    if (status == 'exists'){
        if(confirm('Folder Already Exists -- Overwrite it?')){
            // users chose OK
            alert('OverWrite - OK')
          formData.append('folder_option', 'overwrite')
          fetch('/create_folder', {
            method: 'POST',
            body: formData
          })
          .then(response => response.json())
          .then(data => {console.log(data.status)})
        }
    }
  })
  .catch(error => {
    console.error(error)
  })
}

/************************************************
* handles datetime interval settings - to be used
* to schedule run times for the assigned task on
* server
* @return - None
*************************************************/
date_control.addEventListener('change', event => {
  console.log('DateTime_Control...')
  task_name = document.getElementById('name').value
  if(task_name != ''){
    console.log('task-name set...')
    date_time_ctrl_val = date_control.value
    const formData = new FormData()
    formData.append('folder_name',task_name)
    formData.append('task_interval',date_time_ctrl_val)
    console.log(formData)
    fetch('/create_interval_file', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log(data.status)
    })
  }
  else{
        //signal to user to enter task-name before date selection
        document.getElementById('name').style.borderColor = "red";
        date_control.value = ''
    }
})

/************************************************
* handles configuration upload onto the server
* based on user selection - file to server location
* @return - None
*************************************************/
let file_path = ''
const handleFileUpload = event => {
  const files = event.target.files
  const formData = new FormData()
  var task_name = document.getElementById('name').value
  formData.append('config_file', files[0])
  formData.append('folder_name',task_name)

  fetch('/save_config_schedule', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    file_path = data.path
    console.log(file_path)
  })
  .catch(error => {
    console.error(error)
  })
}

/***************************************************
* handles and detects user configuration file change
* event - used to post and save config on server
* @return - None
****************************************************/
document.querySelector('#schedular_config_input').addEventListener('change', event => {
    handleFileUpload(event)
})

/**************************************************
* handles schedule button click -  add
* new task to be schedule for run at user selected
* time
* @return - Status when task is added
****************************************************/
const button = document.querySelector('#schdl_btn');
button.addEventListener('click', (event) => {
  console.log('**Run button was clicked');
  button.disabled =true;
  let options = {
      method: 'POST',
      headers: {
          "Content-type": "application/json; charset=UTF-8"
      },
      body: JSON.stringify({'folder_name': document.getElementById('name').value, 'interval': date_control.value})
  }
  fetch('/schedule_run_click',options)
    .then(response => {
      console.log(response);
      button.disabled=false           //re-enable button
      alert(' == Task Added == ')
    })
    .catch(function(error) {
      console.log(error);
    });
  console.log(options)
})

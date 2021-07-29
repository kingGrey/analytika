/******************************************
// general declarations get element handles
*******************************************/
let file_path = ''
const cncl_button = document.querySelector('#adhoc_cncl_btn');
const run_button = document.querySelector('#adhoc_run_btn');

/*****************************************
* handles file upload from user
* and file stored locally on machine
* @return - None
*******************************************/
const handleFileUpload = event => {
  const files = event.target.files
  const formData = new FormData()
  formData.append('myFile', files[0])

  fetch('/save_config', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    file_path = data.path
    console.log(`File Stored locally @: ${file_path}`)
  })
  .catch(error => {
    console.error(error)
  })
}

/*********************************************
* on configuration file change post and save
*  to configuration files onto server
*  @return - None
**********************************************/
document.querySelector('#adhoc_config_input').addEventListener('change', event => {
  handleFileUpload(event)
})

/*********************************************
* onclick event listener for ad-hoc run
* @return - None
**********************************************/
run_button.addEventListener('click', (event) => {
  console.log('Run button was clicked');
  run_button.disabled = true;       //disable button

  let log_date = ''
  let options = {
      method: 'POST',
      headers: {
          "Content-type": "application/json; charset=UTF-8"
      },
      body: JSON.stringify({'path': file_path, 'folder_name': log_date, 'run_type':'adhoc'})
  }
  fetch('/adhoc_run_click',options)
    .then(response => response.json())
    .then(data =>{
         console.log(data)
        if(data.includes('Task Completed.')){
            console.log('=======================')
            console.log('FOUND TASK COMPLETED.')
            console.log('=========================')
            alert(' == Run Completed. == ')
        }
        run_button.disabled=false           //re-enable button
    })
    .catch(function(error) {
      console.log(error);
    });
  console.log(options)
});

/**********************************************
* cancel onClick button event - for ad-hoc
* @return None
************************************************/
cncl_button.addEventListener('click', (event) => {
  console.log('Cancel button was clicked');

  let options = {
      method: 'POST',
      headers: {
          "Content-type": "application/json; charset=UTF-8"
      },
      body: JSON.stringify({'path': file_path})
  }
  fetch('/adhoc_cncl_click',options)
    .then(response => {
      console.log(response);
    })
    .catch(function(error) {
      console.log(error);
    });
  console.log(options)
});



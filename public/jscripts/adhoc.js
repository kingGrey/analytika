//get element handles
let file_path = ''
const cncl_button = document.querySelector('#adhoc_cncl_btn');
const run_button = document.querySelector('#adhoc_run_btn');

//handles file upload from user
//and file stored locally on machine
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

// on configuration file change post and save to server
document.querySelector('#adhoc_config_input').addEventListener('change', event => {
  handleFileUpload(event)
})

// onclick event listener for ad-hoc run
run_button.addEventListener('click', (event) => {
  console.log('Run button was clicked');
  const cur_date = new Date()
  console.log(cur_date)
  log_date =  cur_date.getFullYear() +'-'
  log_date+=  cur_date.getMonth().toString().padStart(2,'0') +'-'
  log_date+=  cur_date.getDate().toString().padStart(2,'0') +'_'
  log_date+=  cur_date.getHours().toString().padStart(2,'0') +'-'
  log_date+=  cur_date.getMinutes().toString().padStart(2,'0') +'-'
  log_date+=  cur_date.getSeconds().toString().padStart(2,'0')
  console.log(log_date)

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
        }
    })
    .catch(function(error) {
      console.log(error);
    });
  console.log(options)
});

//cancel onClick button event - for ad-hoc
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



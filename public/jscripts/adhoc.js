
let file_path = ''
const cncl_button = document.querySelector('#adhoc_cncl_btn');
const button = document.querySelector('#adhoc_run_btn');

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
    console.log(file_path)
  })
  .catch(error => {
    console.error(error)
  })
}
// on configuration file change post and save to server
document.querySelector('#adhoc_config_input').addEventListener('change', event => {
  handleFileUpload(event)
})


button.addEventListener('click', (event) => {
  console.log('Run button was clicked');

  let options = {
      method: 'POST',
      headers: {
          "Content-type": "application/json; charset=UTF-8"
      },
      body: JSON.stringify({'path': file_path})
  }
  fetch('/adhoc_run_click',options)
    .then(response => {
      console.log(response);
    })
    .catch(function(error) {
      console.log(error);
    });
  console.log(options)
});


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


const adhoc_btn = document.getElementById('ad_hoc_btn');
const schedule_btn = document.getElementById('schedule_btn');
const report_btn = document.getElementById('report_btn');
const more_info_btn = document.getElementById('more_info')

//
adhoc_btn.addEventListener("click", function () {
    window.location = './adhoc.html'
    console.log("Ad-hoc Button clicked");
});
schedule_btn.addEventListener("click", function () {
    console.log("Scheduler Button clicked");
    window.location = './scheduler.html'
});
report_btn.addEventListener("click", function () {
    console.log("Report Button clicked");
    window.location = './report.html'
});

more_info_btn.addEventListener('click', function(){
    //alert('Clicked.')
})
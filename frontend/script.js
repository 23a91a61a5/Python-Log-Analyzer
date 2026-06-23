async function uploadLog() {

const fileInput = document.getElementById("logFile");

if(fileInput.files.length===0){
alert("Select a log file");
return;
}

const formData=new FormData();

formData.append(
"file",
fileInput.files[0]
);

const response=
await fetch(
"http://127.0.0.1:5000/analyze",
{
method:"POST",
body:formData
}
);

const data=
await response.json();

document.getElementById(
"result"
).innerHTML=`

<h3>Analysis Result</h3>

<p>Total Logs:
${data.total_logs}</p>

<p>INFO:
${data.INFO}</p>

<p>WARNING:
${data.WARNING}</p>

<p>ERROR:
${data.ERROR}</p>

`;
}
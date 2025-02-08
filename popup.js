document.addEventListener('DOMContentLoaded', () => {
  const dropZone = document.getElementById('dropZone');
  const addEventsButton = document.getElementById('addEvents');
  let uploadedFile = null;

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');

    handleFile(e.dataTransfer.files[0]);
  });

  dropZone.addEventListener('click', () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.pdf,.txt';
    fileInput.style.display = 'none';

    fileInput.addEventListener('change', (e) => {
      handleFile(e.target.files[0]);
    });

    document.body.appendChild(fileInput);
    fileInput.click();
    document.body.removeChild(fileInput);
  });

  addEventsButton.addEventListener('click', () => {
    if (!uploadedFile) {
      alert('Please drag and drop a file first!');
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      const text = e.target.result;
      const events = parseSyllabus(text); 
      
      chrome.identity.getAuthToken({ interactive: true }, (token) => {
        if (chrome.runtime.lastError) {
          console.error(chrome.runtime.lastError);
          return;
        }
        events.forEach((event) => addEvent(token, event)); 
        alert('Events added to Google Calendar!');
      });
    };

    if (uploadedFile.type === 'application/pdf') {
      reader.readAsArrayBuffer(uploadedFile);
    } else {
      reader.readAsText(uploadedFile);
    }
  });

  function parseSyllabus () {
    console.log("YRURURURURRR");
  }

  function handleFile(file){
    if (file && (file.type === 'application/pdf' || file.type === 'text/plain')) {
      uploadedFile = file;
      dropZone.innerHTML = `<p>File ready: ${file.name}</p>`;
    } else {
      alert('Please upload a PDF or text file.');
    }
  }
});

// const progress = document.querySelector(".progress-done")
// const input = document.querySelector(".input")
// const maxInput = document.querySelector(".maxInput")
// let total = 0;
// let max = 0;

// function changeWidth() {
//     progress.style.width = `${(total / max) * 100}%`;
//     progress.innerText = `${Math.ceil((total / max) * 100)}%`;
// }

// input.addEventListener("keyup", function ()  {
//     total = parseInt(input.value, 10)
//     changeWidth();
// });

// maxInput.addEventListener("keyup", function ()  {
//     max = parseInt(maxInput.value, 10)
//     changeWidth();
    
// });


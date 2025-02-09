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

  addEventsButton.addEventListener('click', async () => {
    if (!uploadedFile) {
      alert('Please upload a file first!');
      return;
    }

    try {
      const events = await parseSyllabus(uploadedFile);

      chrome.identity.getAuthToken({ interactive: true, scopes: ["https://www.googleapis.com/auth/calendar"] }, (token) => {
        if (chrome.runtime.lastError) {
          console.error(chrome.runtime.lastError);
          return;
        }

        // Initialize Google API client
        gapi.load('client:auth2', async () => {
          await gapi.auth2.init({
            client_id: '362501526390-7vh92smbie9m7jd1mh0q1o7j7qf5n6pf.apps.googleusercontent.com'
          });
          gapi.client.setToken({ access_token: token });

          // Add events to Google Calendar
          events.forEach((event) => addEvent(event));
        });
      });
    } catch (error) {
      console.error('Error processing file:', error);
      alert('Failed to process the file.');
    }
  });

  async function parseSyllabus(file) {
    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const response = await fetch('http://127.0.0.1:5000/extract_events', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const parsedData = await response.json();
      console.log('Parsed events:', parsedData);

      return parsedData.events || [];  // Ensure it returns an array
    } catch (error) {
      console.error('Error sending syllabus to backend:', error);
      return [];
    }
  }

  function handleFile(file) {
    if (file && (file.type === 'application/pdf' || file.type === 'text/plain')) {
      uploadedFile = file;
      dropZone.innerHTML = `<p>File ready: ${file.name}</p>`;
    } else {
      alert('Please upload a valid PDF or text file.');
    }
  }

  function addEvent(event) {
    const eventData = {
      'summary': event.name,
      'start': {
        'date': `${event.month.toString().padStart(2, '0')}-${event.day.toString().padStart(2, '0')}`,
      },
      'end': {
        'date': `${event.month.toString().padStart(2, '0')}-${event.day.toString().padStart(2, '0')}`,
      },
    };

    gapi.client.calendar.events.insert({
      'calendarId': 'primary',
      'resource': eventData,
    }).then((response) => {
      console.log('Event created: ' + response.result.htmlLink);
      alert('Event added to your Google Calendar!');
    }).catch((error) => {
      console.error('Error creating event:', error);
      alert('Failed to add event to Google Calendar.');
    });
  }
});

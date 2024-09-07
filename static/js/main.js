/**
 * Handles WebSocket events for real-time email import and display.
 *
 * @param {WebSocket} ws - The WebSocket connection to the server.
 * @param {HTMLElement} progressBar - The progress bar element to update.
 * @param {HTMLElement} progressMessage - The progress message element to update.
 * @param {HTMLElement} emailsBody - The container element to append email rows.
 */
const ws = new WebSocket('ws://localhost:8000/ws/mails/');
const progressBar = document.querySelector('.progress-bar-inner');
const progressMessage = document.getElementById('progress-message');
const emailsBody = document.getElementById('emails-body');

ws.onopen = function() {
    console.log('Connected to WebSocket');
    ws.send(JSON.stringify({type: 'import'}));
};

ws.onmessage = function(event) {
    try {
        const data = JSON.parse(event.data);

        if (data.type === 'progress') {
            progressBar.style.width = data.progress + '%';
            progressMessage.textContent = data.message;

            // Timer to hide the progress bar after 5 seconds of inactivity
            clearTimeout(window.progressTimeout);
            window.progressTimeout = setTimeout(() => {
                progressBar.style.width = '0%';
                progressMessage.textContent = '';
            }, 5000);

        } else if (data.type === 'message') {
            const email = JSON.parse(data.message);
            const row = document.createElement('div');
            row.classList.add('row');

            const subjectCell = document.createElement('div');
            subjectCell.classList.add('col');
            subjectCell.textContent = email.subject;

            const dateSentCell = document.createElement('div');
            dateSentCell.classList.add('col');
            dateSentCell.textContent = new Date(email.date_sent).toLocaleString();

            const dateReceivedCell = document.createElement('div');
            dateReceivedCell.classList.add('col');
            dateReceivedCell.textContent = new Date(email.date_received).toLocaleString();

            const bodyCell = document.createElement('div');
            bodyCell.classList.add('col');
            bodyCell.textContent = email.body.substring(0, 50) + '...';

            const attachmentsCell = document.createElement('div');
            attachmentsCell.classList.add('col');

            if (email.attachments.length > 0) {
                email.attachments.forEach(attachment => {
                    const link = document.createElement('a');
                    link.href = `/attchmnt/${attachment}`;
                    link.textContent = attachment;
                    link.target = '_blank';
                    attachmentsCell.appendChild(link);
                    attachmentsCell.appendChild(document.createElement('br'));
                });
            }

            row.appendChild(subjectCell);
            row.appendChild(dateSentCell);
            row.appendChild(dateReceivedCell);
            row.appendChild(bodyCell);
            row.appendChild(attachmentsCell);

            emailsBody.appendChild(row);
        } else if (data.error) {
            console.error('Error:', data.error);
        }
    } catch (error) {
        console.error('Error processing message:', error);
    }
};

ws.onerror = function(error) {
    console.error('WebSocket Error:', error);
};

ws.onclose = function() {
    console.log('WebSocket connection closed');
};

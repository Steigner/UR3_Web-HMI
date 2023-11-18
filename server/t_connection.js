const alertPlaceholder = document.getElementById('alert_placeholder');
const appendAlert = (message, type) => {
    // Clear existing alerts
    alertPlaceholder.innerHTML = '';
  
    // Create and append the new alert
    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('');
  
    alertPlaceholder.append(wrapper);
};

const connectButton = document.getElementById('connectButton');
const modalElement = document.getElementById('exampleModal2');
const bsModal = new bootstrap.Modal(modalElement);

// Add a click event listener to the "Connect" button
connectButton.addEventListener('click', function () {
    // Get the value from the input field
    const ipAddress = document.getElementById('recipient-name').value;

    // Using fetch API
    fetch('http://localhost:5000/publish_ip/'+ String(ipAddress))
        .then(response => response.json())
        .then(
            data => {
                console.log(data);
                const status = data.status || 'error';
                const message = data.message || 'Unknown error';

                // Display the status in the alert
                appendAlert(message, status);
                bsModal.hide();
            } 
        )
        .catch((error) => {
        console.error('Error:', error);
    });


    // Use the ipAddress as needed, for example, you can log it to the console
    console.log('IP Address:', ipAddress);
});

document.getElementById('disconnect').addEventListener('click', function() {
    // Using fetch API
    fetch('http://localhost:5000/disconnect')
        .then(response => response.json())
        .then(
            data => {
                console.log(data);
                const status = data.status || 'error';
                const message = data.message || 'Unknown error';

                // Display the status in the alert
                appendAlert(message, status);
            } 
        )
        .catch((error) => {
        console.error('Error:', error);
    });
});


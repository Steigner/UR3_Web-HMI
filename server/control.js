const alertPlaceholder = document.getElementById('alert_placeholder');

var buttonIds = [
    "x+", "x-",
    "y+", "y-",
    "z+", "z-",
    "rx+", "rx-",
    "ry+", "ry-",
    "rz+", "rz-"
];

// Add event listeners to all buttons
for (var i = 0; i < buttonIds.length; i++) {
    let button = document.getElementById(buttonIds[i]);
    let intervalId;

    button.addEventListener('mousedown', function(event) {
        var data = event.target.id;
        intervalId = setInterval(function() {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "http://localhost:5000/receive_command", true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ "data": data }));
        }, 100); // Send data every 100ms = 0.1 second
    });

    // Stop sending data when button is released
    button.addEventListener('mouseup', function() {
        clearInterval(intervalId); 
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://localhost:5000/receive_command", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        for(var k=0; k < 3; k++){
            xhr.send(JSON.stringify({ "data": "stop" }));
        }
    });
}

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
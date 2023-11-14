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
            xhr.open("POST", "http://localhost:5000/receive_string", true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ "data": data }));
        }, 100); // Send data every 100ms = 0.1 second
    });

    // Stop sending data when button is released
    button.addEventListener('mouseup', function() {
        clearInterval(intervalId); 
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://localhost:5000/receive_string", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ "data": "stop" }));
    });
}

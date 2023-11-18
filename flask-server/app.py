from flask import Flask, Response
from flask import request, jsonify
from flask_cors import CORS
from control import Robot_Control
import json
import time

# Initialize the Robot Control module
Robot_Control.init()

# Create a Flask app
app = Flask(__name__)
# Enable CORS for all routes
CORS(app) 

# Route to publish the robot's IP address
@app.route('/publish_ip/<ip_address>')
def publish_ip(ip_address):
    # Connect to the robot using the provided IP address
    result = Robot_Control.connect(ip_adress=ip_address)
    if result:
        return jsonify({"status": "success", "message": "Robot is connected."})
    else:
        return jsonify({"status": "warning", "message": "Wrong IP address."})

# Route to disconnect from the robot
@app.route('/disconnect')
def disconnect():
    # Disconnect from the robot
    Robot_Control.disconnect()
    return jsonify({"status": "success", "message": "Robot is disconnected."})

# Route to receive commands from the client
@app.route('/receive_command', methods=['POST'])
def receive_command():
    # Check if the robot is currently reconnecting
    if Robot_Control.reconnecting:
        return jsonify({"status": "error", "message": "Robot is currently reconnecting."})

    # Extract data from the JSON request
    data = request.get_json()["data"]
    print(f"Received data: {data}")

    # Submit the received data to the Robot Control module
    result = Robot_Control.sub_data(data=data)

    # If result is 1, initiate a reconnect process
    if result == 1:
        Robot_Control.reconnecting = True
        Robot_Control.reconnect()
        Robot_Control.reconnecting = False

    return jsonify({"status": "success"})

# Route to stream digital data from the robot
@app.route('/digital')
def digital():
    def event_stream():
        # Continuous loop to read robot position and stream data
        while True:
            data = Robot_Control.read_robot_pos()
            time.sleep(0.01)
            yield 'data: {}\n\n'.format(json.dumps(data))

    # Return the event stream as a text/event-stream response
    return Response(event_stream(), mimetype="text/event-stream")

# Run the Flask app on host '0.0.0.0' and port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

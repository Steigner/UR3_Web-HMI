from flask import Flask, Response
from flask import request, jsonify
from flask_cors import CORS
from control import Robot_Control
import json
import time

Robot_Control.init()

app = Flask(__name__)
CORS(app)

@app.route('/publish_ip/<ip_address>')
def publish_ip(ip_address):
    result = Robot_Control.connect(ip_adress=ip_address)
    if result:
        return jsonify({"status": "success", "message": "Robot is connected."})
    else:
        return jsonify({"status": "warning", "message": "Wrong IP adress."})

@app.route('/disconnect')
def disconnect():
    Robot_Control.disconnect()
    return jsonify({"status": "success", "message": "Robot is disconnected."})

@app.route('/receive_command', methods=['POST'])
def receive_command():

    if Robot_Control.reconnecting:
        return jsonify({"status": "error", "message": "Robot is currently reconnecting."})

    data = request.get_json()["data"]
    print(f"Received data: {data}")
    result = Robot_Control.sub_data(data=data)
    
    if result == 1:
        Robot_Control.reconnecting = True
        Robot_Control.reconnect()
        Robot_Control.reconnecting = False

    return jsonify({"status": "success"})

@app.route('/digital')
def digital():
    def event_stream():
        while True:
            data = Robot_Control.read_robot_pos()
            time.sleep(0.01)
            yield 'data: {}\n\n'.format(json.dumps(data))

    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
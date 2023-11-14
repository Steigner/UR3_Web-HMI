from flask import Flask, Response
from flask import request, jsonify
from flask_cors import CORS
from setup_zmq import setup_zmq
import json

app = Flask(__name__)
CORS(app)

socket_sub, socket_pub = setup_zmq()

@app.route('/receive_string', methods=['POST'])
def receive_string():
    data = request.get_json()["data"]
    # print(f"Received data: {data}")
    socket_pub.send_pyobj(data)
    return jsonify({"status": "success"})

@app.route('/digital')
def digital():
    def event_stream():
        while True:
            data = socket_sub.recv_pyobj()
            # print(data)
            yield 'data: {}\n\n'.format(json.dumps(data))

    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
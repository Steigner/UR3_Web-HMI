import zmq

def setup_zmq():
    # Create a ZMQ context
    context = zmq.Context()

    socket_sub = context.socket(zmq.SUB)
    socket_sub.connect("tcp://ur-rtde-read:6000")
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, '')

    socket_pub = context.socket(zmq.PUB)
    socket_pub.bind("tcp://*:9000")

    return socket_sub, socket_pub
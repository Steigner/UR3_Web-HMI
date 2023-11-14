import rtde_receive
import zmq
import time

class Robot_Read(object):
    def __init__(self):
        self.__rtde_r = rtde_receive.RTDEReceiveInterface("192.168.19.128")

    def __set_up_zmq(self):
        context = zmq.Context()
        socket_pub = context.socket(zmq.PUB)
        socket_pub.bind("tcp://*:6000")

        return socket_pub
    
    def read_robot_tcp(self):
        rtde_r = self.__rtde_r
        return rtde_r.getActualTCPPose()
    
    def read_robot_pos(self):
        rtde_r = self.__rtde_r
        socket = self.__set_up_zmq()

        while True:
            data = rtde_r.getActualQ()
            time.sleep(0.01)
            # print(data)
            socket.send_pyobj(data)


if __name__ == "__main__":
    robot = Robot_Read()
    print("Robot connected - Reader", flush=True)
    robot.read_robot_pos()
import rtde_control
import zmq

class Robot_Control(object):
    def __init__(self):
        self.__rtde_c = rtde_control.RTDEControlInterface("192.168.19.128")
        self.const_mov = 0.05
        self.const_rot = 0.15

    def __set_up_zmq(self):
        context = zmq.Context()
        socket_sub = context.socket(zmq.SUB)
        socket_sub.connect("tcp://flask-server:9000")
        socket_sub.setsockopt_string(zmq.SUBSCRIBE, '')

        return socket_sub
    
    def sub_data(self):
        socket_sub = self.__set_up_zmq()
        const_mov = self.const_mov
        const_rot = self.const_rot
        
        while True:
            data = socket_sub.recv_pyobj()
            print(data)

            speed_vector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            t_start = self.__rtde_c.initPeriod()

            match data:
                case "x+":
                    speed_vector[0] = const_mov
                case "x-":
                    speed_vector[0] = -const_mov

                case "y+":
                    speed_vector[1] = const_mov

                case "y-":
                    speed_vector[1] = -const_mov

                case "z+":
                    speed_vector[2] = -const_mov

                case "z-":
                    speed_vector[2] = const_mov

                case "rx+":
                    speed_vector[3] = const_rot

                case "rx-":
                    speed_vector[3] = -const_rot

                case "ry+":
                    speed_vector[4] = const_rot

                case "ry-":
                    speed_vector[4] = -const_rot

                case "rz+":
                    speed_vector[5] = const_rot

                case "rz-":
                    speed_vector[5] = -const_rot

                case "stop":
                    speed_vector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

                case _:
                    speed_vector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            self.__rtde_c.jogStart(speed_vector, self.__rtde_c.FEATURE_TOOL)
            self.__rtde_c.waitPeriod(t_start)

if __name__ == "__main__":
    robot = Robot_Control()
    print("Robot connected", flush=True)
    robot.sub_data()
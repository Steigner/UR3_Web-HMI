import rtde_control
import rtde_receive

class Robot_Control(object):
    @classmethod
    def init(cls):
        # Initialize class variables
        cls.reconnecting = False
        cls.__rtde_c = None
        cls.__rtde_r = None
        cls.__const_mov = 0.05  # Constant for linear movement
        cls.__const_rot = 0.15  # Constant for rotational movement

    @classmethod
    def connect(cls, ip_adress):
        try:
            # Attempt to connect to the robot
            cls.__rtde_c = rtde_control.RTDEControlInterface(ip_adress)
            cls.__rtde_r = rtde_receive.RTDEReceiveInterface(ip_adress)

            if cls.__rtde_c.isConnected() and cls.__rtde_r.isConnected():
                print("[INFO] Robot is connected")
                return True
        except:
            print("[ERROR] Wrong IP address")
            return False

    @classmethod
    def disconnect(cls):
        try:
            # Attempt to disconnect from the robot
            cls.__rtde_c.disconnect()
            cls.__rtde_r.disconnect()
            print("[INFO] Robot is disconnected")
        except AttributeError:
            print("[WARNING] Robot is not connected")

    @classmethod
    def reconnect(cls):
        # Reconnect to the robot's control interface
        rtde_c = cls.__rtde_c
        print("[INFO] Control Panel was interrupted on UR Polyscope side.", flush=True)
        rtde_c.disconnect()
        rtde_c.reconnect()

    @classmethod
    def read_robot_pos(cls):
        # Read the current robot position
        if cls.__rtde_r is None:
            return [0, 0, 0, 0, 0, 0]
        elif not cls.__rtde_r.isConnected():
            return [0, 0, 0, 0, 0, 0]
        else:
            return cls.__rtde_r.getActualQ()

    @classmethod
    def sub_data(cls, data):
        # Handle the received command and perform corresponding robot movements
        const_mov = cls.__const_mov
        const_rot = cls.__const_rot
        rtde_c = cls.__rtde_c

        if not rtde_c.isConnected():
            return 0  # Indicate not connected

        if not rtde_c.isProgramRunning():
            return 1  # Indicate program not running

        # Initialize speed vector for robot movements
        speed_vector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        t_start = rtde_c.initPeriod()

        # Match the received data to corresponding movements
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

        # Start jogging with the calculated speed vector
        rtde_c.jogStart(speed_vector, rtde_c.FEATURE_TOOL)
        rtde_c.waitPeriod(t_start)

        return 2  # Indicate successful command processing

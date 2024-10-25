
class Robot(object):
    """Defines the Arlo robot API
    
       DISCLAIMER: This code does not contain error checking - it is the responsibility
       of the caller to ensure proper parameters and not to send commands to the 
       Arduino too frequently (give it time to process the command by adding a short sleep wait
       statement). Failure to do some may lead to strange robot behaviour.
       
       In case you experience trouble - consider using only commands that do not use the wheel 
       encoders.
    """ 
    def __init__(self, port = '/dev/ttyACM0'):
        """The constructor port parameter can be changed from default value if you want
           to control the robot directly from your labtop (instead of from the on-board raspberry 
           pi). The value of port should point to the USB port on which the robot Arduino is connected."""
        print("Running ... dummy robot")
        
    def __del__(self):
        print("Shutting down the dummy robot ...")
        
        
    def send_command(self, cmd, sleep_ms=0.0):
        """Sends a command to the Arduino robot controller"""
        print("dummy robot cmd: ", cmd)

        
    def go_diff(self, powerLeft, powerRight, dirLeft, dirRight):
        """Start left motor with motor power powerLeft (in {0, [30;127]} and the numbers must be integer) and direction dirLeft (0=reverse, 1=forward)
           and right motor with motor power powerRight (in {0, [30;127]} and the numbers must be integer) and direction dirRight (0=reverse, 1=forward).
        
           The Arlo robot may blow a fuse if you run the motors at less than 40 in motor power, therefore choose either 
           power = 0 or 30 < power <= 127.
           
           This does NOT use wheel encoders."""
        print("go_diff: ", powerLeft, powerRight, dirLeft, dirRight)
        
    def stop(self):
        """Send a stop command to stop motors. Sets the motor power on both wheels to zero.
        
           This does NOT use wheel encoders."""
        print("stop")


    
    def read_sensor(self, sensorid):
        """Send a read sensor command with sensorid and return sensor value. 
           Will return -1, if error occurs."""
        print("read_sensor: ", sensorid)
        return 0

    def read_front_ping_sensor(self):
        """Read the front sonar ping sensor and return the measured range in milimeters [mm]"""
        print("read_front_ping_sensor")
        return 0
        
    def read_back_ping_sensor(self):
        """Read the back sonar ping sensor and return the measured range in milimeters [mm]"""
        print("read_back_ping_sensor")
        return 0
        
    def read_left_ping_sensor(self):
        """Read the left sonar ping sensor and return the measured range in milimeters [mm]"""
        print("read_left_ping_sensor")
        return 0
        
    def read_right_ping_sensor(self):
        """Read the right sonar ping sensor and return the measured range in milimeters [mm]"""
        print("read_right_ping_sensor")
        return 0

    

    
        


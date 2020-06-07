#Nathan Lemus and Shawn Leones

#!/usr/bin/python
import time
import serial
import rospy #for talker/ listener
from geometry_msgs.msg
import Twist #for talker/ listener

# 1-127, 64 is stop ch 1
# 128-255, 192 is stop ch 2
# 0 stops both

Left = 0
Right = 0


serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)
while True:
print("UART running. Press CTRL+C to exit.")
serial_port.write(Left)
serial_port.write(Right)


#subscriber
def listener():
    rospy.init_node('isc_joy/manual_control', anonymous=True)
    rospy.Subscriber("/manual_control_vel", Twist, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


#
def callback(msg):
    x = msg.linear.x #msg.msg.linear.x?
    z = msg.angular.z
    rospy.loginfo('x: {}, z: {}'.format(x,z))
    fX = round(x)
    fZ = round(z)
    Conversion(fX, fZ)


#rounds twist inputs to -1 => 1; step = 0.1
def round(f):
    f = (f*10)
    if f > 0:
        var = math.ceil(f)
    else:
        var = math.floor(f)
    return (var/10)


#duty cycle percentage for each channel
def Conversion(i, j):
    if i >= 0:
        i = (64+((127*i)/2))
    else:
        i = (64-((127*i)/2))

    #sets left and right for no turning
    Left = i
    Right = i+128

    if j >= 0:
        j = (64+((127*j)/2))
    else:
        j = (64-((127*j)/2))

    if j > 65:
        Left += j/2
        Right -= j/2
    else if j < 63:
        Left -= j/2
        Right += j/2
    else:
        Left = i
        Right = i+128

from pymavlink import mavutil
import time
import socket
import keyboard

# New UDP socket connection
# Setting as client for the moment
udp_ip = "0.0.0.0" # Replace with UDP server IP
udp_port = 15000    # Replace with UDP server port

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((udp_ip, udp_port))

udp_ip = "192.168.2.2"
# --out udpout:192.168.2.1:14660 in http://192.168.2.2:2770/mavproxy list
pymavlink = mavutil.mavlink_connection('udpin:0.0.0.0:14770')
# ensure valid connection
pymavlink.wait_heartbeat()

heartbeat = mavutil.periodic_event(1) # 1 Hz heartbeat
display = mavutil.periodic_event(5) # 5 Hz output (every 0.2 seconds)

start = time.time()
duration = 160 # seconds

motor_speedInt_p = 100     # Motor speed of bottom motor (pitch)
motor_speedInt_r = 100     # Motor speed of top motor (roll)
motor_speed = (str(motor_speedInt_p) + ' ' + str(motor_speedInt_r)).encode()

print("Set-up Complete")
while time.time() - start < duration:
    if heartbeat.trigger():
        pymavlink.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_GCS,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0,0,0)
        
        sock.sendto(motor_speed, (udp_ip,udp_port))

    # read messages every iteration (to not fall behind)
    att = pymavlink.recv_match(type='ATTITUDE', blocking=True)
    
    if display.trigger():
        print(f"Roll: {att.roll}    Pitch: {att.pitch}")
        print(f"Motor Speed: {motor_speedInt_p} {motor_speedInt_r}")
    
    # Break loop if spacebar is pressed
    if keyboard.is_pressed(' '):
        break

# Return to home position (0, 0)
home_command = ('   ').encode()
sock.sendto(home_command, (udp_ip,udp_port))

# Close connection    - This might help the issue where it doesn't open again
sock.close()

    
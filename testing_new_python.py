from pymavlink import mavutil
import time
import socket
import math
import keyboard
import select
import re

# New UDP socket connection
# Setting as client for the moment
udp_ip = "0.0.0.0" # Replace with UDP server IP
#udp_ip = "192.168.2.2"
udp_port = 15000    # Replace with UDP server port

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((udp_ip, udp_port))

# Setting a timeout for the socket
# sock.settimeout(0.1)
sockets_list = [sock]

udp_ip = "192.168.2.2"
# --out udpout:192.168.2.1:14660 in http://192.168.2.2:2770/mavproxy list
pymavlink = mavutil.mavlink_connection('udpin:0.0.0.0:14770')
# ensure valid connection
pymavlink.wait_heartbeat()

heartbeat = mavutil.periodic_event(1) # 1 Hz heartbeat
display = mavutil.periodic_event(5) # 5 Hz output (every 0.2 seconds)

start = time.time()
duration = 160 # seconds

p_set_point = math.radians(5)
r_set_point = math.radians(0)
P = 800     # Proportional gain 200

motor_speedInt_p = 0
motor_speedInt_r = 0
motor_speed = (str(motor_speedInt_p) + ' ' + str(motor_speedInt_r)).encode()
motor_speed_prev = (str(motor_speedInt_p) + ' ' + str(motor_speedInt_r)).encode()

# Defining Pitch and Roll
pitch_error = 0
roll_error = 0
 
# Define a buffer to hold incoming data
data_buffer = ""

print("Set-up Complete")
while time.time() - start < duration:
    if heartbeat.trigger():
        pymavlink.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_GCS,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0,0,0)
        
        # Adding in check to see if the previous motor speed is same as new motor speed
        if motor_speed != motor_speed_prev:
            sock.sendto(motor_speed, (udp_ip, udp_port))
            motor_speed_prev = motor_speed
        
    if display.trigger():
        print(f"Roll: {att.roll}    Pitch: {att.pitch}")
        print(f"Pitch Error: {pitch_error}")
        print(f"Roll Error: {roll_error}")
        
    # read messages every iteration (to not fall behind)
    att = pymavlink.recv_match(type='ATTITUDE', blocking=False)

    # Drain any old data from the buffer before processing new data
    try:
        while True:
            # This will drain the buffer and clear any old data that may have accumulated
            data, addr = sock.recvfrom(1024)  # 1024 bytes is the buffer size
    except BlockingIOError:
        # Continue when there is no more data in the buffer
        pass

    # Check for incoming data
    readable, _, _ = select.select(sockets_list, [], [], 0.05)  # 0.1 seconds timeout
    for s in readable:
        if s is sock:
            try:
                data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
                print(f"Raw data {data}") 
                print(f"Raw data decoded {data.decode()}") 
                data_buffer += data.decode()  # Append incoming data to the buffer
                 
                # Split buffer into lines and process each complete line
                lines = data_buffer.split('\n')
                data_buffer = lines[-1]  # Keep the last incomplete line in the buffer
                for line in lines[:-1]:  # Process complete lines
                    line = line.strip()  # Remove leading/trailing whitespace
                    if line:  # Ensure line is not empty
                        # Use regex to extract two numbers
                        matches = re.findall(r'(-?\d+)', line)
                        if len(matches) >= 2:
                            position_p = int(matches[0])
                            position_r = int(matches[1])
                            print(f"Position P (steps): {position_p}    Position R (steps): {position_r}")
            except Exception as e:
                print(f"Error receiving data: {e}")


    if att is not None:
        # Generate control signal
        # Pitch Error (Bottom motor)
        pitch_error = p_set_point - att.pitch
        motor_speedInt_p = int(P * pitch_error)
        motor_speed_p = str(motor_speedInt_p).encode()
        # Roll Error (Top motor)
        roll_error = r_set_point - att.roll
        motor_speedInt_r = int(P * roll_error)
        motor_speed_r = str(motor_speedInt_r).encode()
        motor_speed = (str(motor_speedInt_p) + ' ' + str(motor_speedInt_r)).encode()
        print(f"Motor Speed: {motor_speedInt_p} {motor_speedInt_r}")

        # Break loop if spacebar is pressed
    if keyboard.is_pressed(' '):
        break

# Return to home position (0, 0)
home_command = ('   ').encode()
sock.sendto(home_command, (udp_ip,udp_port))

# Close connection
sock.close()
        

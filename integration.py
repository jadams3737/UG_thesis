from pymavlink import mavutil
import time
import socket
import keyboard
import math
import csv

data = []   # For storing pitch and roll data  
filename = 'results/pool_control_zero_negfive3.csv'
K_p = 100    # Proportional constant for P controller
# pitch_target = -5   # degrees       TEST 1
# roll_target = 0   # degrees         TEST 1
pitch_target = 0   # degrees        TEST 2
roll_target = -5   # degrees        TEST 2
# pitch_target = 0   # degrees       TEST 3
# roll_target = 0   # degrees        TEST 3

def collectData(pitch, roll):
    timestamp = time.time()
    data.append([timestamp, pitch, roll])

def exportData():
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Pitch', 'Roll'])  # Write header
        writer.writerows(data)  # Write the data

def main():
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
    control = mavutil.periodic_event(5)

    start = time.time()
    duration = 160 # seconds

    control_mode = False

    multiplier = 100000  # For converting a small decimal to a large one
    pitch_SP = int(math.radians(pitch_target) * multiplier)  # Convert large decimal to integer
    roll_SP = int(math.radians(roll_target) * multiplier)  # Convert large decimal to integer
    pitch_roll_msg = ('   ').encode()   # Initilise as a go home command

    home_command = ('   ').encode()
    forward_msg = ('f').encode()
    back_msg = ('b').encode()
    right_msg = ('r').encode()
    left_msg = ('l').encode()
    forward_right_msg = ('fr').encode()
    forward_left_msg = ('fl').encode()
    back_right_msg = ('br').encode()
    back_left_msg = ('bl').encode()

    print("Set-up Complete")
    while time.time() - start < duration:
        if heartbeat.trigger():
            pymavlink.mav.heartbeat_send(
                mavutil.mavlink.MAV_TYPE_GCS,
                mavutil.mavlink.MAV_AUTOPILOT_INVALID,
                0,0,0)
            
        # read messages every iteration (to not fall behind)
        att = pymavlink.recv_match(type='ATTITUDE', blocking=True)
        pitch_int = int(att.pitch * -multiplier)
        roll_int = int(att.roll * multiplier)

        pitch_deg = round(math.degrees(att.pitch), 2)
        roll_deg = round(math.degrees(att.roll), 2)
        collectData(pitch_deg, roll_deg)
            
        if display.trigger():
            print(f"Pitch (deg): {pitch_deg}    Roll (deg): {roll_deg}")

        if control.trigger() and control_mode:
            pitch_roll_msg = (str(pitch_int) + ' ' + str(roll_int) + ' ' + 
                                str(pitch_SP) + ' ' + str(roll_SP) + ' ' + str(K_p)).encode()
            sock.sendto(pitch_roll_msg, (udp_ip, udp_port))
        
        # Begin movement using controller if 'c' is pressed
        if keyboard.is_pressed('c'):
            print("Control mode activated")
            control_mode = True
        
        # Test moving to end points
        if keyboard.is_pressed('f'):
            control_mode = False
            print("Forward test")
            sock.sendto(forward_msg, (udp_ip, udp_port))
        
        if keyboard.is_pressed('b'):
            control_mode = False
            print("Back test")
            sock.sendto(back_msg, (udp_ip, udp_port))

        if keyboard.is_pressed('l'):
            control_mode = False
            print("Left test")
            sock.sendto(left_msg, (udp_ip, udp_port))

        if keyboard.is_pressed('r'):
            control_mode = False
            print("Right test")
            sock.sendto(right_msg, (udp_ip, udp_port))

        if keyboard.is_pressed('1'):
            control_mode = False
            print("Forward Right test")
            sock.sendto(forward_right_msg, (udp_ip, udp_port))
        
        if keyboard.is_pressed('2'):
            control_mode = False
            print("Forward Left test")
            sock.sendto(forward_left_msg, (udp_ip, udp_port))

        if keyboard.is_pressed('3'):
            control_mode = False
            print("Back Right test")
            sock.sendto(back_right_msg, (udp_ip, udp_port))

        if keyboard.is_pressed('4'):
            control_mode = False
            print("Back Left test")
            sock.sendto(back_left_msg, (udp_ip, udp_port))

        #  Send home command
        if keyboard.is_pressed(' '):
            control_mode = False
            print("Returning to home position")
            sock.sendto(home_command, (udp_ip,udp_port))

        #  Exit control mode
        if keyboard.is_pressed('e'):
            control_mode = False

        #  Quit program
        if keyboard.is_pressed('q'):
            break

    # Send home command to ensure it is always turned off in home position
    sock.sendto(home_command, (udp_ip,udp_port))

    # Close connection
    sock.close()

    # Export data
    exportData()


if __name__ == "__main__":
    main()
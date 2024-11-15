motor_speedInt = 50

#motor_speed = bytes([motor_speedInt])
motor_speed = str(motor_speedInt).encode()

print("Motor speed int")
print(motor_speedInt)

print("Motor Speed byte")
print(motor_speed)

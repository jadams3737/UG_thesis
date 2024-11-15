#include "MotorControl.hpp"

// runSpeed() does one step, hence it is used 
// in many places to ensure smooth movement

void setup() {
    Serial.begin(19200);
    setupMotors(stepper1);
    setupMotors(stepper2);
}

void loop() {  
  // Check if data is available to read from the serial port
  if (Serial.available() > 0) {
    int index = 0;
    // Read data until two intervals of 5ms have passed with no byte received
    while (Serial.available() > 0 || index < commandLength - 1 && intervalNoByte < 3) {
      currentMillis = millis();
      // Attempt to read a byte after 5ms (allows time for data to arrive):
      if (currentMillis - previousMillis >= interval){
        previousMillis = currentMillis;
        char incomingByte = Serial.read();
        // Store Byte if available:
        if (isDigit(incomingByte) || incomingByte == '-' || incomingByte == ' ' || incomingByte == '.' || (incomingByte >= 'a' &&  incomingByte <= 'z')) { // Accept digits, negative sign, letters, fullstop
          command[index] = incomingByte;
          index++;
          intervalNoByte = 0;
        } else {  // Else count intervals with no Byte:
          intervalNoByte++;
        }
      }
      // Prevent collision with actuator ends
      stopAtEnds(velocity1, stepper1);
      stopAtEnds(velocity2, stepper2);
      // Call run speed while waiting for 5ms
      stepper1.runSpeed();  
      stepper2.runSpeed(); 
    }
    command[index] = '\0'; // Null-terminate the string

    // If the command is '   ', return to (0,0):
    if (strcmp(command, "   ") == 0) {
      goToPos = true;
      stepper1.moveTo(0);
      stepper2.moveTo(0);
    } 
    else if (strcmp(command, "f") == 0) {
      goToPos = true;
      stepper1.moveTo(maxPosition);
      stepper2.moveTo(0);
    }
    else if (strcmp(command, "b") == 0) {
      goToPos = true;
      stepper1.moveTo(-maxPosition);
      stepper2.moveTo(0);
    }
    else if (strcmp(command, "l") == 0) {
      goToPos = true;
      stepper1.moveTo(0);
      stepper2.moveTo(-maxPosition);
    }
    else if (strcmp(command, "r") == 0) {
      goToPos = true;
      stepper1.moveTo(0);
      stepper2.moveTo(maxPosition);
    }
    else if (strcmp(command, "fr") == 0) {
      goToPos = true;
      stepper1.moveTo(maxPosition);
      stepper2.moveTo(maxPosition);
    }
    else if (strcmp(command, "fl") == 0) {
      goToPos = true;
      stepper1.moveTo(maxPosition);
      stepper2.moveTo(-maxPosition);
    }
    else if (strcmp(command, "br") == 0) {
      goToPos = true;
      stepper1.moveTo(-maxPosition);
      stepper2.moveTo(maxPosition);
    }
    else if (strcmp(command, "bl") == 0) {
      goToPos = true;
      stepper1.moveTo(-maxPosition);
      stepper2.moveTo(-maxPosition);
    }
    else {  // Else, set velocity:
      goToPos = false;
      sscanf(command, "%d %d %d %d %d", &pitch, &roll, &pitch_OP, &roll_OP, &K_p); 
      // Serial.print(pitch);  Serial.print(' '); Serial.print(roll);  Serial.print(' '); 
      // Serial.print(pitch_OP);  Serial.print(' '); Serial.print(roll_OP); 
      // Serial.print(' '); Serial.println(K_p);
      velocity1 = pid(pitch, pitch_OP);
      velocity2 = pid(roll, roll_OP);
      stepper1.setSpeed(velocity1);
      stepper2.setSpeed(velocity2);
      // Serial.print("Velocity1: "); Serial.println(velocity1); Serial.print("Velocity2: "); Serial.println(velocity2);
    }
  }
  // Prevent collision with actuator ends
  // Serial.println("Running Stop at Ends");
  stopAtEnds(velocity1, stepper1);
  stopAtEnds(velocity2, stepper2);

  // Run movement commands:
  if (goToPos == true){
    // Serial.println("Going Home");
    stepper1.run();
    stepper2.run();
    if (stepper1.run() == false && stepper2.run() == false)
      goToPos = false;
  }
  else {
    stepper1.runSpeed(); 
    stepper2.runSpeed(); 
  }
}

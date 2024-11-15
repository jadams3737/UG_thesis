#include "MotorSet.hpp"

long positionN1 = 0;
long positionN2 = 0;

void setup() {
    Serial.begin(19200);
    setupMotors(stepper1);
    setupMotors(stepper2);
    // Serial.println("To set the motor speeds, send a string like this {motor1_speed} {motor2_speed}");
}

void loop() {  
  position1 = stepper1.currentPosition();
  position2 = stepper2.currentPosition();
  if (stepper1.speed() != 0 || stepper2.speed() != 0) {
    //Serial.print(position1);  Serial.print(" "); Serial.println(position2);   // Sends position via serial
    positionN1 = positionN1 + 1;
    positionN2 = positionN2 + 1;
    Serial.print(positionN1);  Serial.print(" "); Serial.println(positionN2);
  }

  // Check if data is available to read from the serial port
  if (Serial.available() > 0) {
    int index = 0;
    stepper1.runSpeed(); 
    stepper2.runSpeed(); 
    while (Serial.available() > 0 && index < commandLength - 1) {
      stepper1.runSpeed(); 
      stepper2.runSpeed(); 
      char incomingByte = Serial.read();
      if (isDigit(incomingByte) || incomingByte == '-' || incomingByte == ' ') { // Accept digits and negative sign
        command[index] = incomingByte;
        index++;
      }
      stepper1.runSpeed(); 
      stepper2.runSpeed(); 
      delay(5); // Give some time for the data to come in
    }
    command[index] = '\0'; // Null-terminate the string
    sscanf(command, "%d %d", &velocity1, &velocity2); 

    stepper1.setSpeed(velocity1);
    stepper2.setSpeed(velocity2);
    stepper1.runSpeed(); 
    stepper2.runSpeed();  

    // If the command is three spaces, return to (0,0)
    if (strcmp(command, "   ") == 0) {
      Serial.println("GO HOME");
      goHome = true;
      stepper1.moveTo(0);
      stepper2.moveTo(0);
      stepper1.setSpeed(100);
      stepper2.setSpeed(100);
      stepper1.runSpeed(); 
      stepper2.runSpeed(); 
    }

    // Serial.print("Motor speed 1 set to: "); Serial.println(velocity1);
    // Serial.print("Motor speed 2 set to: "); Serial.println(velocity2);
  }

  // Serial.print("Current speed motor 1: "); Serial.println(stepper1.speed());

  stopAtEnds(position1, velocity1, stepper1);
  stopAtEnds(position2, velocity2, stepper2);

  if (goHome == true){
    // Serial.println("Going Home");
    stepper1.run();
    stepper2.run();
    if (stepper1.run() == false && stepper2.run() == false)
      goHome = false;
  }

  stepper1.runSpeed(); 
  stepper2.runSpeed(); 
}

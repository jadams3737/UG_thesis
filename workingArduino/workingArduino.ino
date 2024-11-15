#include <AccelStepper.h>

// Define the serial command buffer size
const int commandLength = 10;
char command[commandLength];

const int StepX = 2;
const int DirX = 5;

// Define the stepper motor and the pins that are connected to
AccelStepper stepper1(AccelStepper::DRIVER, StepX, DirX); // (Typeof driver: with 2 pins, STEP, DIR)

long position;
long maxPosition = 8000;

float velocity;

void setup() {
  // Initialize serial communication at 115200 bits per second
  Serial.begin(19200);

  // Set maximum acceleration for the stepper
  stepper1.setAcceleration(500);
  stepper1.setMaxSpeed(1000);
  // max position 8242
  stepper1.setCurrentPosition(0);

  // Set an initial speed (optional, can be 0 to start with no movement)
  stepper1.setSpeed(0);

  // Print a welcome message to the serial monitor
  Serial.println("Send a number to set the motor speed:");

}

void loop() {
  // Run the stepper motor continuously at the set speed
  
  position = stepper1.currentPosition();
  // Serial.print(position);
  // Serial.print("\n");
  // Serial.print(maxPosition);
  // Serial.print("\n");
  

  // Check if data is available to read from the serial port
  if (Serial.available() > 0) {
    // Read the incoming number (velocity)
    Serial.println("Loop ran with serial input ");
    int index = 0;
    while (Serial.available() > 0 && index < commandLength - 1) {
      char incomingByte = Serial.read();
      if (isDigit(incomingByte) || incomingByte == '-') { // Accept digits and negative sign
        command[index] = incomingByte;
        index++;
      }
      delay(5); // Give some time for the data to come in
    }
    command[index] = '\0'; // Null-terminate the string

    // Convert the string to an integer (motor velocity)
    velocity = atof(command);

    // Set the motor speed (steps per second)
    stepper1.setSpeed(velocity);

    // Provide feedback on the set velocity
    Serial.print("Motor speed set to: "); Serial.println(velocity);
  }


  if (position > maxPosition && velocity <= 0) {
    stepper1.setSpeed(velocity);
    //Serial.println("First if ");
    //Serial.println(position);
  }
  else if (position < -maxPosition && velocity >= 0) {
    stepper1.setSpeed(velocity);
    //Serial.println("Second if ");
  }
  else if (abs(position) <= (maxPosition + 200)) {
    stepper1.setSpeed(velocity);
    //Serial.println("Third if ");
  }
  else {
    stepper1.setSpeed(0);
    //Serial.println("Fourth if ");
  }
  stepper1.runSpeed(); 
}
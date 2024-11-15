#include "MotorSet.hpp"

void setupMotors(AccelStepper &stepper)
{
    stepper.setAcceleration(500);
    stepper.setMaxSpeed(400);     // Was originally 1000
    stepper.setCurrentPosition(0);   // max position 8242
    // stepper.setSpeed(0);
}

void stopAtEnds(long position, long velocity, AccelStepper &stepper)
{
  if (position > maxPosition && velocity <= 0) {
    // Do nothing, this is a valid velocity
    stepper.setSpeed(velocity);
  }
  else if (position < -maxPosition && velocity >= 0) {
    // Do nothing, this is a valid velocity
    stepper.setSpeed(velocity);
  }
  else if (abs(position) <= (maxPosition + 100)) {
    // Do nothing, this is a valid position
  }
  else {
    stepper.setSpeed(0);
  }
}

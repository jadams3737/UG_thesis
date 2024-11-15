// #pragma once

#ifndef MOTOR_HPP
#define MOTOR_HPP

#include <AccelStepper.h>

// Define the pins that are connected to the stepper motor
const int StepX = 2;
const int StepY = 3;
const int DirX = 5;
const int DirY = 6;

// Define the stepper motor and the pins they are connected to
AccelStepper stepper1(AccelStepper::DRIVER, StepX, DirX); // (Typeof driver: with 2 pins, STEP, DIR)
AccelStepper stepper2(AccelStepper::DRIVER, StepY, DirY); // (Typeof driver: with 2 pins, STEP, DIR)

// Define the serial command buffer size
const int commandLength = 10;
char command[commandLength];

// Variable declarations
bool goHome = false;
long maxPosition = 8000;
long position1;
long position2;
int velocity1 = 0;
int velocity2 = 0;

// NEW
int velocity1prev = 0;
int velocity2prev = 0;



// Function prototypes
void stopAtEnds(long position, long velocity, AccelStepper &stepper);
void setupMotors(AccelStepper &stepper);


#endif
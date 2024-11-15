// #pragma once

#ifndef MOTOR_HPP
#define MOTOR_HPP

#include <AccelStepper.h>
#include <BasicLinearAlgebra.h>

// Reading Serial messages
unsigned long currentMillis = 0;
unsigned long previousMillis = 0;
const long interval = 5;
int intervalNoByte = 0;

// Stepper Motor Pins
const int StepX = 2;
const int StepY = 3;
const int StepZ = 4;
const int DirX = 5;
const int DirY = 6;
const int DirZ = 7;
const int StepA = 12;
const int DirA = 13; 

// Stepper Motors
AccelStepper stepper1(AccelStepper::DRIVER, StepX, DirX); // (Typeof driver: with 2 pins, STEP, DIR)
AccelStepper stepper2(AccelStepper::DRIVER, StepY, DirY); // (Typeof driver: with 2 pins, STEP, DIR)

// Serial command buffer size
const int commandLength = 30;
char command[commandLength];

// Motor variables
bool goToPos = false;
long maxPosition = 8500;
long position1;
long position2;
float velocity1 = 0;
float velocity2 = 0;

// Control variables
int pitch = 0;
int roll = 0;
int pitch_OP = 0;
int roll_OP = 0;
int K_p = 1;  // Proportional constant for PID
BLA::Matrix<4, 8> K = {   // Gain for LQR control, taken from Matlab script
  11.3888, 10.1032, -8.42003e-15, -2.30865e-15, 13.4846, 1.1655, 1.21399e-15, -1.16936e-15,
  1.18353e-14, 6.21183e-15, 11.3889, 10.1355, 2.64156e-16, 7.49826e-17, 13.4842, 1.18333,
  10.1562, 0.527051, 1.15049e-14, 1.1497e-15, 15.4875, 6.6247, -1.12429e-14, -1.46842e-15,
  1.12124e-14, 6.15434e-15, 10.1566, 0.55552, 1.42873e-16, 8.3693e-16, 15.4875, 6.62153
};

// Function prototypes
void stopAtEnds(long position, long velocity, AccelStepper &stepper);
void setupMotors(AccelStepper &stepper);
float pid(int current, int set_point);
float lqr(int pitch, int roll, int pitch_SP, int roll_SP);

#endif
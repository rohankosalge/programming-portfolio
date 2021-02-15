/*----------------------------------------------------------------------------*/
/*                                                                            */
/*    Module:       main.cpp                                                  */
/*    Author:       rohankosalge                                              */
/*    Created:      Thu Dec 24 2020                                           */
/*    Description:  V5 project                                                */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#include "vex.h"
using namespace vex;

// ---- START VEXCODE CONFIGURED DEVICES ----
motor leftFront = motor(PORT4, true);
motor rightFront = motor(PORT5, true);
motor leftBack = motor(PORT2, true);
motor rightBack = motor(PORT6, true);
motor bottomRollers = motor(PORT3, ratio6_1, false);
motor topRollers = motor(PORT20, ratio6_1, false);
motor leftIntake = motor(PORT8, false);
motor rightIntake = motor(PORT15, true);

inertial gyrosensor = inertial(PORT7);
controller Controller = controller();
// ---- END VEXCODE CONFIGURED DEVICES ----

const double INTAKESENSE = 1.00;
const double XSENSE = 0.5;
const double YSENSE = 0.5;

// ---- INTAKES ----

// runs intakes indefinitely (until user stops)
void run_intakes(){
  leftIntake.spin(forward, INTAKESENSE*100, pct);
  rightIntake.spin(forward, INTAKESENSE*100, pct);
  bottomRollers.spin(forward, 100, pct);  // ball is able to get in the robot 
}

// runs intakes for specified amount of time
void run_intakes_for(int milliseconds){
  leftIntake.spin(forward, INTAKESENSE*100, pct);
  rightIntake.spin(forward, INTAKESENSE*100, pct);
  bottomRollers.spin(forward, 100, pct);
  wait(milliseconds, msec);
  leftIntake.stop(hold);
  rightIntake.stop(hold);
}

// reverses intakes indefinitely (until user stops)
void reverse_intakes(){
  leftIntake.spin(reverse, INTAKESENSE*100, pct);
  rightIntake.spin(reverse, INTAKESENSE*100, pct);
  bottomRollers.spin(reverse, 100, pct);
}

// reverses intakes for specified amount of time
void reverse_intakes_for(int milliseconds){
  leftIntake.spin(reverse, INTAKESENSE*100, pct);
  rightIntake.spin(reverse, INTAKESENSE*100, pct);
  bottomRollers.spin(reverse, 100, pct);
  wait(milliseconds, msec);
  leftIntake.stop(hold);
  rightIntake.stop(hold);
}

// stops intakes
void stop_intakes(){
  leftIntake.stop(hold);
  rightIntake.stop(hold);
}

// ---- ROLLERS ----

// launches rollers indefinitely (until user stops)
void launch_rollers(){
  topRollers.spin(forward, 100, pct);
  bottomRollers.spin(forward, 100, pct);
}

// launches rollers for specified amount of time 
void launch_rollers_for(int milliseconds){
  topRollers.spin(forward, 100, pct);
  bottomRollers.spin(forward, 100, pct);
  wait(milliseconds, msec);
  topRollers.stop(hold);
  bottomRollers.stop(hold);
}

// poops rollers indefinitely (until user stops)
void poop_rollers(){
  topRollers.spin(reverse, 100, pct);
  bottomRollers.spin(forward, 100, pct);
}

// poops rollers for specified amount of time
void poop_rollers_for(int milliseconds){
  topRollers.spin(reverse, 100, pct);
  bottomRollers.spin(forward, 100, pct);
  wait(milliseconds, msec);
  topRollers.stop(hold);
  bottomRollers.stop(hold);
}

// stops rollers
void stop_rollers(){
  topRollers.stop(hold);
  bottomRollers.stop(hold);
}

// flip the hood up
void formulate(int vel, int ms){
  //calibrateGyro();
  // only move top rollers back for a small time
  topRollers.spin(reverse, vel, pct);
  wait(ms, msec);
  topRollers.stop();
}

void userformulate(){
  formulate(50, 500);
}

void shootpooptwo(){
  launch_rollers_for(300);
  run_intakes_for(100);
  launch_rollers_for(300);
  run_intakes_for(100);

  
  reverse_intakes_for(150);

  //poop_rollers_for(250);

}


int main() {
  // Initializing Robot Configuration. DO NOT REMOVE!
  vexcodeInit();

  int drivepos;
  int turnpos;
  int leftunits;
  int rightunits;
  
  while(true){
    drivepos = YSENSE*Controller.Axis3.position();
    turnpos = XSENSE*Controller.Axis1.position();

    leftunits = drivepos + turnpos;
    rightunits = turnpos - drivepos;

    if(leftunits == 0 && rightunits == 0){
      leftFront.stop(coast);
      rightFront.stop(coast);
      leftBack.stop(coast);
      rightBack.stop(coast);
    }else{
      leftFront.spin(forward, leftunits, pct);
      rightFront.spin(forward, rightunits, pct);
      leftBack.spin(forward, leftunits, pct);
      rightBack.spin(forward, rightunits, pct);
    }
    

    Controller.ButtonR2.pressed(run_intakes);
    Controller.ButtonL2.pressed(stop_intakes);
    Controller.ButtonR1.pressed(launch_rollers);
    Controller.ButtonL1.pressed(stop_rollers);
    Controller.ButtonA.pressed(poop_rollers);
    Controller.ButtonY.pressed(reverse_intakes);
    Controller.ButtonX.pressed(userformulate);
    Controller.ButtonRight.pressed(shootpooptwo);
  }

}

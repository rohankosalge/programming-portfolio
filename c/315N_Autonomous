/*----------------------------------------------------------------------------*/
/*                                                                            */
/*    Module:       main.cpp                                                  */
/*    Author:       Rohan Kosalge                                             */
/*    Created:      Thursday, September 26, 2020                              */
/*    Description:  Competition Template                                      */
/*                                                                            */
/*----------------------------------------------------------------------------*/                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

// ---- START VEXCODE CONFIGURED DEVICES ----
// Robot Configuration:
// [Name]               [Type]        [Port(s)]
// leftLine             line          G               
// middleLine           line          A               
// rightLine            line          H               
// bottomLine           line          B               
// ---- END VEXCODE CONFIGURED DEVICES ----
#include "vex.h"
#include <string.h>
#include <math.h>

using namespace vex;

// A global instance of competition
competition Competition;

motor leftFront = motor(PORT4, true);
motor rightFront = motor(PORT5, false);
motor leftBack = motor(PORT2, true);
motor rightBack = motor(PORT6, false);
motor TopRollers = motor(PORT20, ratio6_1, false);
motor BottomRollers = motor(PORT3, ratio18_1, false);
motor leftIntake = motor(PORT8, ratio18_1, false);
motor rightIntake = motor(PORT15, ratio18_1, true);
inertial InertialSensor = inertial(PORT1);
motor_group leftDrive(leftBack, leftFront);
motor_group rightDrive(rightBack, rightFront);
motor_group intakes(leftIntake, rightIntake);
motor_group frontDrive(leftFront, rightFront);
motor_group backDrive(leftBack, rightBack);
controller Controller1 = controller();

// extra motor group only used for roller launching assistance
motor_group rollers(TopRollers, BottomRollers);

// constants
const double SENSE = 0.45; // sensitivity

const double DRIVEP = 70;                   // 30 for under 750 ticks, 50 for (750, 1000), 70 for > 1000
const double DRIVEI = 1;
const double DRIVED = 0;

const double TURNP = 90;
const double TURNI = 1;
const double TURND = 0;
const double TURN_OFFSET = 2;
const long TURN_INTEGRAL_LIMIT = 2000;

const int NUMDRIVEMOTORS = 4;
const long DRIVE_INTEGRAL_LIMIT = 1500;     // 1500 for < 750, 2000 for (750, 1000), 2500 for > 1000
const long DRIVE_PROP_LIMIT = 50000;
const double HEAD_OFFSET = 0.1;
const long OFFSET_VOLTAGE = 600;
const long VOLTAGE_RATE = 10;
const long VOLTAGE_MIN = 1500;
const long TIME_INTERVAL = 2;               // in milliseconds

const int WHITE_REFLECT_PCT = 2;
const int GREY_REFLECT_PCT = 44;
const int THRESH = (WHITE_REFLECT_PCT+GREY_REFLECT_PCT)/2;  // threshold constant takes the average of the color values

// to check whether a wheel is still running in the auton, use this constant to define 
// how many ticks ahead the program will check before stopping
const int TICKSGAP = 10;


void assignDriveMotorsVoltage(double leftSide, double rightSide){
  leftFront.spin(forward, leftSide, vex::voltageUnits::mV);
  rightFront.spin(forward, rightSide, vex::voltageUnits::mV);
  leftBack.spin(forward, leftSide, vex::voltageUnits::mV);
  rightBack.spin(forward, rightSide, vex::voltageUnits::mV);
}

double getAverageVoltage(){
  return ( fabs(leftFront.voltage(vex::voltageUnits::mV)) + fabs(leftBack.voltage(vex::voltageUnits::mV))
           + fabs(rightFront.voltage(vex::voltageUnits::mV)) + fabs(rightBack.voltage(vex::voltageUnits::mV)) ) / NUMDRIVEMOTORS;
}

int getAverageTicks(){
  //return ( fabs(leftFront.position(vex::rotationUnits::raw)) + fabs(leftBack.position(vex::rotationUnits::raw))
               //+ fabs(rightFront.position(vex::rotationUnits::raw)) + fabs(rightBack.position(vex::rotationUnits::raw)) ) / NUMDRIVEMOTORS;

  return (fabs(leftBack.position(vex::rotationUnits::raw)) + fabs(rightBack.position(vex::rotationUnits::raw)) ) / 2;
}

void resetMotors(){
  leftFront.resetPosition();
  leftBack.resetPosition();
  rightFront.resetPosition();
  rightBack.resetPosition();
}

void stopMotors(){
  leftFront.stop(vex::brakeType::hold);
  rightFront.stop(vex::brakeType::hold);
  leftBack.stop(vex::brakeType::hold);
  rightBack.stop(vex::brakeType::hold);
}

int get_line_values(){
  // Key to check line values:
  // 0: if none of the lines are white
  // 1: if one of the lines are white
  // 2: if two of the lines are white
  // 3: if all of the lines are white
  // there should be 2^3, or 8 cases, that are checked. 

  int result;

  int leftval = leftLine.value(pct);
  int middleval = middleLine.value(pct);
  int rightval = rightLine.value(pct);

  if(leftval < THRESH && middleval < THRESH && rightval < THRESH){
    result = 3;
  }else{
    if((leftval < THRESH && middleval < THRESH && rightval >= THRESH) || (leftval < THRESH && middleval >= THRESH && rightval < THRESH) || (leftval >= THRESH && middleval < THRESH && rightval < THRESH)){
      result = 2;
    }else{
      if((leftval < THRESH && middleval >= THRESH && rightval >= THRESH) || (leftval >= THRESH && middleval >= THRESH && rightval < THRESH) || (leftval >= THRESH && middleval < THRESH && rightval >= THRESH)){
        result = 1;
      }else{
        result = 0;
      }
    }
  }

  return result;

}

double safegetheading(){
  double gyroheading = InertialSensor.heading();
  if(gyroheading > 359.7 || gyroheading < 0.3) {gyroheading = 0;}
  return gyroheading;
}

void drivePID(long target_ticks){
  long integral; 
  long derivative;
  long error; 
  long prev_error;
  long prev_ticks;
  double prop_pct;
  double final_volt = 3000.0;
  long cur_ticks;

  error = 0;
  prev_error = 0;
  cur_ticks = 0;
  integral = 0;
  derivative = 0;
  prop_pct = 0;
  prev_ticks = 0;

  resetMotors();

  while(abs(cur_ticks) < abs(target_ticks)){
    
    error = abs(target_ticks)  - abs(cur_ticks);
    prop_pct = ((double) error / (double) abs(target_ticks)) * 100;
    derivative = error - prev_error;
    integral = integral + error;

    if(integral > DRIVE_INTEGRAL_LIMIT) {integral = DRIVE_INTEGRAL_LIMIT;}
    if(error > DRIVE_PROP_LIMIT) { error = DRIVE_PROP_LIMIT; }

    final_volt = (abs(target_ticks)/(target_ticks)) * ((DRIVEP * prop_pct) + (DRIVEI * integral) + (DRIVED * derivative));
    
    assignDriveMotorsVoltage(final_volt, final_volt);
    prev_error = error;
    prev_ticks = cur_ticks;
    wait(2, msec);
    cur_ticks = getAverageTicks();
   
  }
  stopMotors();
  //wait(100,msec);
  // Controller1.Screen.clearScreen();
  // Controller1.Screen.setCursor(0, 0);
  // Controller1.Screen.print("C =%d, P = %d", cur_ticks, prev_ticks);
  // Controller1.Screen.setCursor(2, 0);
  // Controller1.Screen.print("F = %d", getAverageTicks());
}

void drivePIDheading(double p, double i, double d, long integral_limit, long target_ticks, double head, bool check_for_line){
  long integral; 
  long derivative;
  long error; 
  long prev_error;
  long prev_ticks;
  double prop_pct;
  double prev_prop_pct;
  double final_volt = 3000.0;
  long cur_ticks;
  double compare_head = 0;
  double prev_volt;
  double cur_head;

  long prev_interval_ticks = 0;

  error = 0;
  prev_error = 0;
  cur_ticks = 0;
  integral = 0;
  derivative = 0;
  prop_pct = 0;
  prev_prop_pct = 0;
  prev_ticks = 0;
  prev_volt = 0;
  bool is_forward;

  resetMotors();

  if(target_ticks >=0) {is_forward = true;}
  else {is_forward = false;}

  Controller1.Screen.clearScreen();
  Controller1.Screen.setCursor(0, 0);
  Controller1.Screen.print("Start head: %3.2f", head);

  int modcount = 25;  
  int loopcount = 0;
  while(abs(cur_ticks) < abs(target_ticks)){
    compare_head = head;
    
    error = abs(target_ticks)  - abs(cur_ticks);
    prop_pct = ((double) error / (double) abs(target_ticks)) * 100;
    
    if(prev_prop_pct == 0) {derivative = 0;}
    else {derivative = (prop_pct - prev_prop_pct) * 100;}

    integral += error;
    if(i*integral > integral_limit) {integral = integral_limit/i;}
    if(error > DRIVE_PROP_LIMIT) {error = DRIVE_PROP_LIMIT;}

    final_volt = (abs(target_ticks)/(target_ticks)) * ((p * prop_pct) + (i * integral) + (d * derivative));

    if(is_forward){
      if(final_volt - prev_volt > VOLTAGE_RATE*TIME_INTERVAL){
        if ((VOLTAGE_RATE*TIME_INTERVAL) + prev_volt < VOLTAGE_MIN) {final_volt = VOLTAGE_MIN;}
        else {final_volt = (VOLTAGE_RATE*TIME_INTERVAL) + prev_volt;}
      }
    }else{
      if(final_volt - prev_volt < VOLTAGE_RATE*TIME_INTERVAL){
        if (prev_volt - (VOLTAGE_RATE*TIME_INTERVAL) > -VOLTAGE_MIN) {final_volt = -VOLTAGE_MIN;}
        else {final_volt = prev_volt - (VOLTAGE_RATE*TIME_INTERVAL);}
      }
    }


    // if(fabs(final_volt - prev_volt) > VOLTAGE_RATE*TIME_INTERVAL){
    //   if ((VOLTAGE_RATE*TIME_INTERVAL) + fabs(prev_volt) < VOLTAGE_MIN) {final_volt = VOLTAGE_MIN;}
    //   else {final_volt = (VOLTAGE_RATE*TIME_INTERVAL) + fabs(prev_volt);}
    // }

    // if(!is_forward){
    //   final_volt = -final_volt;
    // }
    
    cur_head = InertialSensor.heading();

    if(fabs(head-cur_head) > 180){
      if (cur_head < head) {cur_head += 360;}
      else {compare_head += 360;}
    }

    if(fabs(compare_head-cur_head) > HEAD_OFFSET){
      if(compare_head > cur_head){
        // if the target heading is greater than the current heading, then slightly turn right
        assignDriveMotorsVoltage(final_volt+OFFSET_VOLTAGE, final_volt-OFFSET_VOLTAGE);
      }else{
        // if the target heading is less than the current heading, then slightly turn left
        assignDriveMotorsVoltage(final_volt-OFFSET_VOLTAGE, final_volt+OFFSET_VOLTAGE);
      }
    }else{
      assignDriveMotorsVoltage(final_volt, final_volt);
    }
    
    prev_volt = final_volt;
    prev_prop_pct = prop_pct;
    prev_error = error;
    prev_ticks = cur_ticks;
    wait(TIME_INTERVAL, msec);
    cur_ticks = getAverageTicks();


    loopcount++;
    if(loopcount%modcount == 0){
      if(prev_interval_ticks == cur_ticks){
        break;
      }else{
        prev_interval_ticks = cur_ticks;
      }
    }

    // if line checking is requested, check for line detection every loop
    if(check_for_line){
      int linestatus = get_line_values();
      if(linestatus>=2){
        break;
      }
    }


  }
  Controller1.Screen.setCursor(2, 0);
  Controller1.Screen.print("Final head: %3.2f", InertialSensor.heading());
  Controller1.Screen.setCursor(4, 0);
  Controller1.Screen.print("Differential: %1.2f", fabs(InertialSensor.heading()-head));
  stopMotors();
}

void turnPID(double turn_deg, bool is_right, long turnilim){
  // turn right if true, turn left if false

  double integral = 0;
  double derivative = 0;
  double error = 0;
  double prop_pct = 0;
  double prev_error = 0;
  double final_volt = 0;

  double cur_deg = safegetheading();
  double start_deg = cur_deg;
  double end_deg = 0;
  double prev_deg = cur_deg;
  bool switch_deg = false;
  bool keep_looping = true;

  if (is_right) {end_deg = start_deg + turn_deg;}
  else {end_deg = start_deg - turn_deg;}

  // Controller1.Screen.clearScreen();
  // Controller1.Screen.setCursor(0, 0);
  // Controller1.Screen.print("S: %f", start_deg);
  // Controller1.Screen.setCursor(2, 0);
  // Controller1.Screen.print("E: %f", end_deg);

  while(keep_looping){

    error = turn_deg - fabs(cur_deg - start_deg);
    prop_pct = (error/turn_deg) * 100;
    integral += error;
    derivative = error - prev_error;

    if(integral > turnilim){
      integral = turnilim;
    }

    final_volt = (TURNP * prop_pct) + (TURNI * integral) + (TURND * derivative);

    if(is_right){
      assignDriveMotorsVoltage(final_volt, -final_volt);
    }else{
      assignDriveMotorsVoltage(-final_volt, final_volt);
    }

    prev_error = error;
    prev_deg = cur_deg;
    wait(2, msec);

    cur_deg = safegetheading();

    if(fabs(cur_deg - prev_deg) > 100) {switch_deg = true;}

    if(switch_deg){
      if (is_right) {cur_deg += 360;}
      else {cur_deg -= 360;}
    }

    if(is_right){
      if (cur_deg >= start_deg-TURN_OFFSET && cur_deg <= end_deg) {keep_looping = true;}
      else {keep_looping = false;}
    }else{
      if (cur_deg <= start_deg+TURN_OFFSET && cur_deg >= end_deg) {keep_looping = true;}
      else {keep_looping = false;}
    }
    
  }
  stopMotors();
  //wait(500, msec);
  //InertialSensor.resetHeading();
  // Controller1.Screen.clearScreen();
  // Controller1.Screen.setCursor(0, 0);
  // Controller1.Screen.print("S: %f", start_deg);
  // Controller1.Screen.setCursor(2, 0);
  // Controller1.Screen.print("E: %f", end_deg);    
  // Controller1.Screen.setCursor(4, 0);
  // Controller1.Screen.print("C: %f", cur_deg);
}


void turnPIDheading(double head, long turnilim){
  double cur_head = safegetheading();

  // figures out which direction to turn and modifies the degrees
  if(fabs(head-cur_head) > 180){
    if (cur_head < head) {cur_head += 360;}
    else {head += 360;}
  }

  double deg = head-cur_head;

  if(deg < 0){
    // if the difference is negative, then we turn left
    turnPID(-deg, false, turnilim);
  }else{
    // if the difference is positive, then we turn right
    turnPID(deg, true, turnilim);
  }

  // Controller1.Screen.clearScreen();
  // Controller1.Screen.setCursor(0, 0);
  // Controller1.Screen.print("C: %f", cur_head);
  // Controller1.Screen.setCursor(2, 0);
  // Controller1.Screen.print("T: %f", head);
}


void rforward(long ticks){
  drivePID(ticks);
}

void rback(long ticks){
  drivePID(-ticks);
}

void rright(double deg, long turnilim){
  turnPID(deg, true, turnilim);
}

void rleft(double deg, long turnilim){
  turnPID(deg, false, turnilim);
}

void rturn(double head, long turnilim){
  turnPIDheading(head, turnilim);
}

void rdrive(double ticks, double p, long integral_limit, bool check_for_line){
  drivePIDheading(p, 1, 0, integral_limit, ticks, InertialSensor.heading(), check_for_line);
}

void stop_intakes(){
  // stop intakes and bottom rollers (if they were running)
  intakes.stop();
  BottomRollers.stop();
  //controller_screen_update(0, 0, "Intakes stopped.", false);
}

void start_intakes(int rollers_vel){
  intakes.spin(forward, 100, pct);
  BottomRollers.spin(forward, rollers_vel, pct);
  //controller_screen_update(0, 0, "Intaking...", false);
}

void drive_testing(){
  //InertialSensor.resetHeading();
  //drivePIDheading(1500, InertialSensor.heading());
  //drivePIDheading(2000, InertialSensor.heading());
  start_intakes(100);
  rdrive(3000, 110, 1500, false);
  stop_intakes();
  //wait(1, sec);
  //rdrive(-3000, 100, 1000);
  // rdrive(test_p, 1, 0, 300);
  // wait(500,msec);
  // Controller1.Screen.clearScreen();
  // Controller1.Screen.setCursor(0, 0);
  // Controller1.Screen.print("Ticks: %d", getAverageTicks());
  // Controller1.Screen.setCursor(2, 0);
  // Controller1.Screen.print("Head: %3.2f", InertialSensor.heading());
}

bool is_launching = false;
bool is_pooping = false;

/*---------------------------------------------------------------------------*/
/*                          Pre-Autonomous Functions                         */
/*                                                                           */
/*  You may want to perform some actions before the competition starts.      */
/*  Do them in the following function.  You must return from this function   */
/*  or the autonomous and usercontrol tasks will not be started.  This       */
/*  function is only called once after the V5 has been powered on and        */
/*  not every time that the robot is disabled.                               */
/*---------------------------------------------------------------------------*/

void calibrateGyro(){
  // calibrate the inertial sensor
  InertialSensor.calibrate();
  while(InertialSensor.isCalibrating()){
    wait(100, msec);
  }
  InertialSensor.resetHeading();
}

void pre_auton(void) {
  // Initializing Robot Configuration. DO NOT REMOVE!
  vexcodeInit();

  // All activities that occur before the competition starts
  // Example: clearing encoders, setting servo positions, ...
  calibrateGyro();
  wait(5, sec);
  Controller1.Screen.clearScreen();
  Controller1.Screen.setCursor(2, 2);
  Controller1.Screen.print("done calibrating");
}

/*---------------------------------------------------------------------------*/
/*                              Autonomous Task                              */
/*                                                                           */
/*  This task is used to control your robot during the autonomous phase of   */
/*  a VEX Competition.                                                       */
/*                                                                           */
/*  You must modify the code to add your own robot specific commands here.   */
/*---------------------------------------------------------------------------*/

void reset_motors(){
  leftFront.resetPosition();
  leftBack.resetPosition();
  rightFront.resetPosition();
  rightBack.resetPosition();
}

void controller_screen_update(int cursorX, int cursorY, std::string msg, bool rumble){
  // call this function after every robot function
  // so that the driver knows what is going on

  Controller1.Screen.clearLine();
  Controller1.Screen.clearScreen();
  Controller1.Screen.setCursor(cursorX, cursorY);
  //Controller1.Screen.print(msg);
  if(rumble==true){
    Controller1.rumble("-----");
  }
}

void launch_rollers(double premillis, double seconds){
  rollers.spin(reverse, 100, pct);
  wait(premillis, msec);
  rollers.spin(forward, 100, pct);
  wait(seconds, sec);
  TopRollers.stop();
  BottomRollers.stop();
}

void run_intakes(){
  intakes.spin(forward, 100, pct);
  //controller_screen_update(0, 0, "Intaking...", false);
}

void formulate(int vel, int ms){
  //calibrateGyro();
  // only move top rollers back for a small time
  TopRollers.spin(reverse, vel, pct);
  wait(ms, msec);
  TopRollers.stop();
  TopRollers.spin(forward, vel, pct);
  wait(ms+100, msec);
  TopRollers.stop();
}

// how much offset is needed for the robot to properly get to 
// a certain tower before accurately launching the ball. 
int CTOFF1 = 0;
int ETOFF1 = 60;
int CTOFF2 = 25;
int ETOFF2 = 50;
int CTOFF3 = 25;
int ETOFF3 = 0;
int CTOFF4 = 20;
int ETOFF4 = 0;

void autonomous(void) {
  // ..........................................................................
  // Insert autonomous user code here.

  // unfold hood
  formulate(70, 200);

  InertialSensor.setHeading(90, deg);

  // get the ball in front, turn to the corner tower and launch preload.
  start_intakes(0);
  rdrive(750, 60, 2500, false);
  //stop_intakes();
  rturn(328, 3000);   // Was 328
  //start_intakes(0);
  stop_intakes();
  rdrive(1530, 60, 3000, false);
  //start_intakes(100);
  launch_rollers(0, 0.75);  // Shoot at Tower #1
  //stop_intakes();

  // turn away from the corner tower, move to edge tower and 
  // launch the ball that was previously acquired.
  //start_intakes(100);
  rdrive(-1000, 60, 2500, false);
  //stop_intakes();
  rturn(0, 2000);
  start_intakes(60);
  rdrive(-1850, 40, 3000, false);  // Backing towards Tower #2
  stop_intakes();
  //rturn(180, 2500);
  //rdrive(1900, 60, 2500);
  rturn(270, 2500);
  rdrive(500, 40, 2000, false);
  launch_rollers(0, 1);  // Shoot at Tower #2; changed from 125 to 0

  // // // move back and turn away from edge tower, get ball in front
  // // // and turn to the corner tower, using that ball to launch in.
  rdrive(-250, 35, 1500, false);
  rturn(180, 2500);
  start_intakes(100);
  rdrive(2275, 60, 3000, false);  // Slowed the P a bit since it seems to jerk here. Increased I; Changed P from 50 to 60
  rturn(225, 2500);
  stop_intakes();
  rdrive(850, 55, 3000, false);
  launch_rollers(0, 1); // Shoot at Tower #3; changed from 125 to 0

  // // // move back from corner, turn and move to the second edge tower
  // // // get the ball there, turn and launch it in
  rdrive(-815, 60, 2000, false);
  rturn(89, 3000);
  start_intakes(100);
  rdrive(200, 70, 2700, false);
  rdrive(2050, 70, 2700, true); // Changed P from 60 to 70
  rturn(180, 2500);
  stop_intakes();
  rdrive(400, 40, 1500, false);
  launch_rollers(0, 1);  // Shoot at Tower #4; changed from 125 to 0

  // // // move back from edge tower, move forward so that robot is perpendicular
  // // // to the ball on the wall, then turn and move forward to get it
  rdrive(-300, 40, 1500, false);
  rturn(89, 2700);
  rdrive(1875, 70, 2500, false);
  rturn(180, 2700);
  start_intakes(100);
  rdrive(500, 50, 2000, false);  

  // // // move back, turn and move to the corner tower and launch ball
  rdrive(-500, 50, 500, false);
  stop_intakes();
  rturn(121, 2500);
  rdrive(1300, 70, 3000, false);
  launch_rollers(125, 1); // Shoot at Tower #5; Changed from 0 to 125

  // // // move back from corner tower, turn and move to the ball in front
  // // // launch acquired ball into edge tower
  rdrive(-425, 60, 2000, false);
  rturn(358, 2500);
  start_intakes(80);
  rdrive(2800, 70, 3300, false); // Changed P from 55 to 70
  stop_intakes();
  rturn(90, 2500);
  rdrive(450, 35, 1500, false);
  launch_rollers(125, 1);   // Shoot at Tower #6
  
  // // // move back from edge tower, turn and move to the next ball in front,
  // // // launch that ball into the following corner tower
  rdrive(-325, 40, 1500, false);
  rturn(0, 2500);
  start_intakes(100);
  rdrive(2350, 70, 3300, false); // Changed P from 55 to 70
  rturn(38, 2500);
  stop_intakes();
  rdrive(950, 55, 2500, false);
  launch_rollers(0, 1);  // Shoot at Tower #7; changed from 175 to 0

  // // // move back from corner tower, turn and move to the ball in front
  // // // get ball, turn to final edge tower and shoot
  rdrive(-470, 60, 2000, false);
  rturn(270, 2500);
  start_intakes(100);
  rdrive(200, 50, 3300, false);
  rdrive(2275, 70, 3300, true); // Changed P from 60 to 70
  rturn(0, 2500);
  stop_intakes();
  rdrive(425, 35, 2000, false);
  launch_rollers(0, 1);  // Shoot at Tower #8

  // move back from Tower #8, turn around 180˚ and get ball
  // to shoot in the last tower (middle tower)
  rdrive(-300, 50, 1500, false);
  rturn(178, 2600);
  start_intakes(100);
  rdrive(700, 70, 1500, false);
  rturn(185, 2500);
  rdrive(1000, 110, 3000, false);
  stop_intakes();
  rdrive(-50, 50, 1500, false);
  rturn(150, 2500);
  //rdrive(50, 50, 500, false);
  launch_rollers(200, 1);
  rdrive(-200, 90, 2000, false);

  // ..........................................................................
}

void test_middle_tower(){
  rdrive(-300, 50, 1500, false);
  rturn(180, 2600);
  start_intakes(100);
  rdrive(700, 70, 1500, false);
  rturn(185, 2500);
  rdrive(1000, 110, 3000, false);
  stop_intakes();
  rdrive(-50, 50, 1500, false);
  rturn(150, 2500);
  //rdrive(50, 50, 500, false);
  launch_rollers(200, 1);
  rdrive(-200, 90, 2000, false);
}

/*--------------------------------------------------------------------------------*/
/*                                                                                */
/*                               User Control Task                                */
/*                                                                                */
/*   This task is used to control your robot during the user control phase of     */
/*   a VEX Competition.                                                           */
/*                                                                                */
/*   BETWEEN THIS COMMENT AND THE USERCONTROL VOID ARE THE CONTROLLER FUNCTIONS.  */
/*--------------------------------------------------------------------------------*/

// USER FUNCTIONS

void user_formulate(){
  formulate(20, 375);
}

void user_start_intakes(){
  // start intakes and bottom rollers 50% velocity
  start_intakes(50);
}

void reverse_intakes(){
  // reverse intakes (outtakes)
  intakes.spin(reverse, 100, pct);
  //controller_screen_update(0, 0, "Reversing intakes...", false);
}

void user_launch_rollers(){
  // move top rollers forward, bottom rollers forward
  TopRollers.spin(forward, 100, pct);
  BottomRollers.spin(forward, 100, pct);

  Controller1.Screen.clearLine();
  Controller1.Screen.clearScreen();
  Controller1.Screen.setCursor(0, 0);
  Controller1.Screen.print("Rollers are launching");
}

void user_poop_rollers(){
  // move top rollers back, bottom roller forward
  TopRollers.spin(reverse, 100, pct);
  BottomRollers.spin(forward, 100, pct);
  
  Controller1.Screen.clearLine();
  Controller1.Screen.clearScreen();
  Controller1.Screen.setCursor(0, 0);
  Controller1.Screen.print("Rollers are pooping");
}

void user_stop_rollers(){
  TopRollers.stop();
  BottomRollers.stop();
}

void gyrolog(){
  // list all gyro stats on the controller and then reset the gyro positions. 

  double gyro_heading = InertialSensor.heading(vex::rotationUnits::deg);
  double gyro_ticks = leftFront.position(vex::rotationUnits::raw);

  Controller1.Screen.clearScreen();
  Controller1.Screen.setCursor(0, 0);

  Controller1.Screen.print("Head: %f", gyro_heading);
  Controller1.Screen.setCursor(2, 0);
  Controller1.Screen.print("Ticks: %f", gyro_ticks);

  //InertialSensor.setHeading(0, vex::rotationUnits::deg);
  reset_motors();

}

void usercontrol(void) {
  // User control code here, inside the loop
  while (1) {
    // This is the main execution loop for the user control program.
    // Each time through the loop your program should update motor + servo
    // values based on feedback from the joysticks.

    // ........................................................................
    // Insert user code here. This is where you use the joystick and button values to
    // update your motors, etc.
    // ........................................................................

    int drivePos = Controller1.Axis3.position(percent); // get the driving position (in percent value)
    int turnPos = Controller1.Axis1.position(percent);  // get the turning position (in percent value)

    // use the SCALE constant to reduce the impact of the turn
    float scaledTurnPos = ((turnPos * 100) * SENSE) / 100;
    float leftMtrVals = (drivePos + scaledTurnPos);
    float rightMtrVals = -(scaledTurnPos - drivePos);

    // motor threshold

    if(leftMtrVals > 100){
        leftMtrVals = 100;
    }
    if(leftMtrVals < -100){
        leftMtrVals = -100;
    }
    if(rightMtrVals > 100){
        rightMtrVals = 100;
    }
    if(rightMtrVals < -100){
        rightMtrVals = -100;
    }

    //leftDrive.spin(forward, leftMtrVals, pct);
    //rightDrive.spin(forward, rightMtrVals, pct);

    // Sleep the task for a short amount of time to prevent wasted resources.
    wait(1, msec); 
  }
}

void turn_testing(){
  InertialSensor.setHeading(90, deg);
  rturn(180, 1500);
  wait(5, sec);
  rturn(90, 1500);
  wait(500, msec);
  Controller1.Screen.setCursor(2, 0);
  Controller1.Screen.print("Head: %3.2f", InertialSensor.heading());
}

void line_tracking_testing(){
  start_intakes(100);
  drivePIDheading(50, 1, 0, 3300, 2800, InertialSensor.heading(), true);
  stop_intakes();
}

// Main will set up the competition functions and callbacks.
int main() {
  calibrateGyro();

  Controller1.ButtonL2.pressed(stop_intakes);
  Controller1.ButtonR2.pressed(user_start_intakes);
  Controller1.ButtonA.pressed(user_poop_rollers);
  Controller1.ButtonR1.pressed(user_launch_rollers);
  Controller1.ButtonY.pressed(reverse_intakes);
  Controller1.ButtonL1.pressed(user_stop_rollers);
  Controller1.ButtonX.pressed(user_formulate);
  Controller1.ButtonB.pressed(gyrolog);

  // Testing Buttons
  Controller1.ButtonLeft.pressed(drive_testing);
  Controller1.ButtonRight.pressed(turn_testing);
  Controller1.ButtonUp.pressed(test_middle_tower);
  Controller1.ButtonDown.pressed(line_tracking_testing);
  
  // Set up callbacks for autonomous and driver control periods.
  Competition.autonomous(autonomous);
  Competition.drivercontrol(usercontrol);

  // Run the pre-autonomous function.
  pre_auton();

  // Prevent main from exiting with an infinite loop.
  while (true) {
    wait(100, msec);
  }
}


#include <Servo.h>

Servo servoMotor1; // Create a servo object for motor 1
Servo servoMotor2; // Create a servo object for motor 2

void setup() {
  servoMotor1.attach(9); // Attach motor 1 to pin 9
  servoMotor2.attach(10); // Attach motor 2 to pin 10
  servoMotor1.write(90); 
  servoMotor2.write(90); // Set the initial angle to 90 degrees (midpoint) for motor 2
  Serial.begin(9600);   // Initialize the serial communication
}

void loop() {
  if (Serial.available() >= 2) { // We need to receive two angles separated by a space
    int angle1 = Serial.parseInt(); // Read the first angle value from serial input
    int angle2 = Serial.parseInt(); // Read the second angle value from serial input
    
    // Constrain the angles between 0 and 180 degrees
    angle1 = constrain(angle1, 0, 180);
    angle2 = constrain(angle2, 0, 180);
    
    servoMotor1.write(angle1); // Move motor 1 to the specified angle
    servoMotor2.write(angle2); // Move motor 2 to the specified angle
  }
}

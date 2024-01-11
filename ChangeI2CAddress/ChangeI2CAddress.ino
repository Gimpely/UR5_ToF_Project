/**
 * This example contains a basic setup to start the distance measurement of the VL53L1X
 * with the I2C address changed
 */

#include "VL53L1X_ULD.h"

#define VL53L1X_ULD_I2C_ADDRESS 0x55  // Default address is 0x52

#define VL53L1X_I2C_ADDRESS_1 0x55  // default is 0x52
#define VL53L1X_I2C_ADDRESS_2 0x56

#define TIMING_BUDGET 20      // Allowed values: 15, 20, 33, 50, 100, 200, 500
#define INTER_MEASUREMENT 20  // Must be equal to or more than timing budget

VL53L1X_ULD sensor1;
VL53L1X_ULD sensor2;

uint8_t XSDN1_pin = A2;
uint8_t XSDN2_pin = A3;

void setup() {
  Serial.begin(115200);  // Start the serial port
  Wire.begin();          // Initialize the I2C controller

  pinMode(XSDN1_pin, OUTPUT);  // set XSDN pins as output
  pinMode(XSDN2_pin, OUTPUT);


  digitalWrite(XSDN1_pin, HIGH);  // enable sensor 1
  digitalWrite(XSDN2_pin, LOW);   // disable sensor 2

  VL53L1_Error status;

  status = sensor1.Begin(VL53L1X_I2C_ADDRESS_1);                 // Initialize the sensor, give the special I2C_address to the Begin function
  status |= sensor1.SetTimingBudgetInMs(TIMING_BUDGET);          // Allowed values: 15, 20, 33, 50, 100, 200, 500
  status |= sensor1.SetInterMeasurementInMs(INTER_MEASUREMENT);  // Must be equal to or more than timing budget
  status |= sensor1.SetDistanceMode(Short);                      // Short (up to 1.3m) or Long (up to 4m, lower noise immunity)
  if (status != VL53L1_ERROR_NONE) {
    Serial.println("Could not initialize the sensor1, error code: " + String(status));  // If the sensor could not be initialized print out the error code. -7 is timeout
    while (1) {}
  }
  Serial.print("Sensor1 initialized with address: 0x");
  Serial.println(sensor1.GetI2CAddress(), HEX);

  digitalWrite(XSDN2_pin, HIGH);  // enable sensor 2
  status = sensor2.Begin(VL53L1X_I2C_ADDRESS_2);
  status |= sensor2.SetTimingBudgetInMs(TIMING_BUDGET);          // Allowed values: 15, 20, 33, 50, 100, 200, 500
  status |= sensor2.SetInterMeasurementInMs(INTER_MEASUREMENT);  // Must be equal to or more than timing budget
  status |= sensor2.SetDistanceMode(Short);                      // Short (up to 1.3m) or Long (up to 4m, lower noise immunity)
  if (status != VL53L1_ERROR_NONE) {
    Serial.println("Could not initialize the sensor1, error code: " + String(status));  // If the sensor could not be initialized print out the error code. -7 is timeout
    while (1) {}
  }
  Serial.print("Sensor2 initialized with address: 0x");
  Serial.println(sensor2.GetI2CAddress(), HEX);


  //sensor1.StartRanging();
  //sensor2.StartRanging();
}

void loop() {
  // Checking if data is available. This can also be done through the hardware interrupt. See the ReadDistanceHardwareInterrupt for an example
  uint8_t dataReady1, dataReady2;
  uint16_t distance1, distance2;
  ERangeStatus rangeStatus1, rangeStatus2;



  while (1) {
    if (Serial.available()) {
      Serial.read();
      sensor1.StartRanging();
      sensor2.StartRanging();

      while (0) {
        sensor1.CheckForDataReady(&dataReady1);
        sensor2.CheckForDataReady(&dataReady2);
        if (dataReady1) {
          sensor1.GetDistanceInMm(&distance1);
          Serial.println("Distance 1 in mm: " + String(distance1));

          sensor1.GetRangeStatus(&rangeStatus1);
          Serial.println("Range status 1: " + String((uint8_t)rangeStatus1));

          sensor1.ClearInterrupt();  // After reading the results reset the interrupt to be able to take another measurement
          sensor1.StopRanging();
        }
        if (dataReady2) {
          sensor2.GetDistanceInMm(&distance2);
          Serial.println("Distance 2 in mm: " + String(distance2));

          sensor2.GetRangeStatus(&rangeStatus2);
          Serial.println("Range status 2: " + String((uint8_t)rangeStatus2));

          sensor2.ClearInterrupt();  // After reading the results reset the interrupt to be able to take another measurement
          sensor2.StopRanging();
        }
      }

      // read sesnor 1
      dataReady1 = false;
      while (!dataReady1) { sensor1.CheckForDataReady(&dataReady1); }
      sensor1.GetDistanceInMm(&distance1);
      //Serial.println("Distance 1 in mm: " + String(distance1));

      sensor1.GetRangeStatus(&rangeStatus1);
      //Serial.println("Range status 1: " + String((uint8_t)rangeStatus1));

      sensor1.ClearInterrupt();  // After reading the results reset the interrupt to be able to take another measurement
      sensor1.StopRanging();


      // read sesnor 2
      dataReady2 = false;
      while (!dataReady2) { sensor2.CheckForDataReady(&dataReady2); }
      sensor2.GetDistanceInMm(&distance2);
      //Serial.println("Distance 2 in mm: " + String(distance2));

      sensor2.GetRangeStatus(&rangeStatus2);
      //Serial.println("Range status 2: " + String((uint8_t)rangeStatus2));

      sensor2.ClearInterrupt();  // After reading the results reset the interrupt to be able to take another measurement
      sensor2.StopRanging();

      Serial.print("0,");
      Serial.print(distance1);
      Serial.print(',');
      Serial.print(rangeStatus1);
      Serial.print(',');
      Serial.print("1,");
      Serial.print(distance2);
      Serial.print(',');
      Serial.print(rangeStatus2);
      Serial.println();
    }
  }
}

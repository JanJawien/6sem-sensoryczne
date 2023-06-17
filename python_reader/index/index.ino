#include "DFRobot_BloodOxygen_S.h"
#include <Adafruit_LSM6DS3TRC.h>

// Initialize Pulsoximeter - MAX30102 with I2C
#define I2C_COMMUNICATION 
#ifdef  I2C_COMMUNICATION
  #define I2C_ADDRESS    0x57
  DFRobot_BloodOxygen_S_I2C MAX30102(&Wire ,I2C_ADDRESS);
#else
  #if defined(ARDUINO_AVR_UNO) || defined(ESP8266)
    SoftwareSerial mySerial(4, 5);
    DFRobot_BloodOxygen_S_SoftWareUart MAX30102(&mySerial, 9600);
  #else
    DFRobot_BloodOxygen_S_HardWareUart MAX30102(&Serial1, 9600); 
  #endif
#endif

Adafruit_LSM6DS3TRC lsm6ds3trc;




int tempPin = A0; // Temperature sensor - LM35-DZ

int lm35Value; 
sensors_event_t accel;
sensors_event_t gyro;
sensors_event_t temp;

const int ADA_BATCH_SIZE = 200;




void setup() { 
  Serial.begin(115200);
  // Serial.println("Begin setup()");
  
  ////////////// Begin Initialize MAX30102 ///////////////
  // Serial.println("Begin Init MAX30102");
  while(!MAX30102.begin())
  {
    // Serial.println("Init failed, retry in 5s");
    delay(5000);
  }
  // Serial.println("Init success!");
  
  MAX30102.sensorStartCollect();
  
  // Serial.println("End Init MAX30102");
  //////////////  End Initialize MAX30102  ///////////////

  ////////////// Start Initialize LSM6DS3TR-C ///////////////
  // Serial.println("Start Init LSM6DS3TR-C");

  if (!lsm6ds3trc.begin_I2C()) {
    // Serial.println("Failed to find LSM6DS3TR-C chip");
    while (1) {
      delay(10);
    }
  }
  // Serial.println("LSM6DS3TR-C Found!");

  lsm6ds3trc.configInt1(false, false, true); // accelerometer DRDY on INT1
  lsm6ds3trc.configInt2(false, true, false); // gyro DRDY on INT2

  // Serial.println("End Init LSM6DS3TR-C");
  //////////////  End Initialize LSM6DS3TR-C  ///////////////

  // Serial.println("End setup()");
}

void loop() { 
  //// Read values from max and lm35
  lm35Value = analogRead(tempPin);
  MAX30102.getHeartbeatSPO2();
  
  //// Print values to serial
  Serial.print("0 ");
  Serial.print(lm35Value);
  Serial.print(" ");
  Serial.print(MAX30102.getTemperature_C());
  Serial.print(" ");
  Serial.print(MAX30102._sHeartbeatSPO2.SPO2);
  Serial.print(" ");
  Serial.println(MAX30102._sHeartbeatSPO2.Heartbeat);

  delay(4000/ADA_BATCH_SIZE); // 4000/200 = 20[ms] // 50fps



  //// Read values from ada and print for x times
  for(int i=0; i<ADA_BATCH_SIZE; ++i){
    lsm6ds3trc.getEvent(&accel, &gyro, &temp);

    Serial.print("1 ");
    Serial.print(temp.temperature);
    Serial.print(" ");
    Serial.print(accel.acceleration.x);
    Serial.print(" ");
    Serial.print(accel.acceleration.y);
    Serial.print(" ");
    Serial.println(accel.acceleration.z);
    
    delay(4000/ADA_BATCH_SIZE); // 4000/200 = 20[ms] // 50fps
  } 
}
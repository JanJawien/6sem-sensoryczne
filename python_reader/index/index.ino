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

const int ADA_BATCH_SIZE = 10;
float ada_temp[ADA_BATCH_SIZE];
float ada_x[ADA_BATCH_SIZE];
float ada_y[ADA_BATCH_SIZE];
float ada_z[ADA_BATCH_SIZE];



void setup() { 
  Serial.begin(9600);
  Serial.println("Begin setup()");
  
  ////////////// Begin Initialize MAX30102 ///////////////
  Serial.println("Begin Init MAX30102");
  while(!MAX30102.begin())
  {
    Serial.println("Init failed, retry in 5s");
    delay(5000);
  }
  Serial.println("Init success!");
  
  MAX30102.sensorStartCollect();
  
  Serial.println("End Init MAX30102");
  //////////////  End Initialize MAX30102  ///////////////

  ////////////// Start Initialize LSM6DS3TR-C ///////////////
  Serial.println("Start Init LSM6DS3TR-C");

  if (!lsm6ds3trc.begin_I2C()) {
    Serial.println("Failed to find LSM6DS3TR-C chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("LSM6DS3TR-C Found!");

  lsm6ds3trc.configInt1(false, false, true); // accelerometer DRDY on INT1
  lsm6ds3trc.configInt2(false, true, false); // gyro DRDY on INT2

  Serial.println("End Init LSM6DS3TR-C");
  //////////////  End Initialize LSM6DS3TR-C  ///////////////

  Serial.println("End setup()");
}

void loop() { 
  //// Read values form sensors
  lm35Value = analogRead(tempPin);
  MAX30102.getHeartbeatSPO2();
  
  for(int i=0; i<ADA_BATCH_SIZE; ++i){
    lsm6ds3trc.getEvent(&accel, &gyro, &temp);
    ada_temp[i] = temp.temperature;
    ada_x[i] = accel.acceleration.x  ;  
    ada_y[i] = accel.acceleration.y  ;  
    ada_z[i] = accel.acceleration.z    ;
    
    delay(4000/ADA_BATCH_SIZE); // 4000/200 = 20[ms] // 50fps
  }




  //// Print values to serial
  Serial.print("{\"lm35_temp\":\"");
  Serial.print(lm35Value);
  Serial.print("\",\"max_temp\":\"");
  Serial.print(MAX30102.getTemperature_C());    
  Serial.print("\",\"max_spo2\":\"");
  Serial.print(MAX30102._sHeartbeatSPO2.SPO2);
  Serial.print("\",\"max_bpm\":\"");
  Serial.print(MAX30102._sHeartbeatSPO2.Heartbeat);
  
  Serial.print("\",\"ada_temp\":[");
  for(int i=0; i<ADA_BATCH_SIZE; ++i) Serial.print((String)"\""+ada_temp[i]+"\",");    
  Serial.print("],\"ada_x\":[");
  for(int i=0; i<ADA_BATCH_SIZE; ++i) Serial.print((String)"\""+ada_x[i]+"\",");
  Serial.print("],\"ada_y\":[");
  for(int i=0; i<ADA_BATCH_SIZE; ++i) Serial.print((String)"\""+ada_y[i]+"\",");
  Serial.print("],\"ada_z\":[");
  for(int i=0; i<ADA_BATCH_SIZE; ++i) Serial.print((String)"\""+ada_z[i]+"\",");
  Serial.println("]}");



  //// Rest and repeat
  delay(20); 
}
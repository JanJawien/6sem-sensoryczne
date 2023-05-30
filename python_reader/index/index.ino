#include "DFRobot_BloodOxygen_S.h"

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

int tempPin = A0; // Temperature sensor - LM35-DZ

int lm35Value; 



void setup() { 
  Serial.begin(9600);
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

  // Serial.println("End setup()");
}

void loop() { 
  //// Read values form sensors
  lm35Value = analogRead(tempPin);
  MAX30102.getHeartbeatSPO2();



  //// Print values to serial
  Serial.print("{\"lm35_temp\":\"");
  Serial.print(lm35Value);
  Serial.print("\",\"max_temp\":\"");
  Serial.print(MAX30102.getTemperature_C());    
  Serial.print("\",\"max_spo2\":\"");
  Serial.print(MAX30102._sHeartbeatSPO2.SPO2);
  Serial.print("\",\"max_bpm\":\"");
  Serial.print(MAX30102._sHeartbeatSPO2.Heartbeat);
  Serial.println("\"}");



  //// Rest and repeat
  delay(500); 
}
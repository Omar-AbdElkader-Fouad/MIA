#include <Wire.h>
#include <SoftwareSerial.h>

const int rxPin = 7;
const int txPin = 6;
SoftwareSerial mySerial(rxPin, txPin);

void setup() {
  Serial.begin(4800);
  Wire.begin();
  mySerial.begin(4800);
}

void loop() {
  Wire.requestFrom(8, 5);
  
  while (Wire.available()) {
    char c = Wire.read();
    mySerial.print(c);
  }
  mySerial.println();
  delay(500);   
}

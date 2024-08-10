#include <SoftwareSerial.h>

const int rxPin = 7;
const int txPin = 6;
SoftwareSerial mySerial(rxPin, txPin);

void setup() {
  Serial.begin(4800);
  mySerial.begin(4800);
}

void loop() {
  if (mySerial.available()) {
    String data = mySerial.readStringUntil('\n');
    Serial.println(data);
    delay(1000);
  }
}

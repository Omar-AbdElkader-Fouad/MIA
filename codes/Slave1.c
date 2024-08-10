#include <Wire.h>

void setup() {
  Serial.begin(4800);
  Wire.begin(8);
  Wire.onRequest(requestfunc);
}

void loop() {
  delay(100);
}

void requestfunc() {
  Wire.write("Hello");
}

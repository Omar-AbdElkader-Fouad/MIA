const int photoresistorPin = A0;
const int buzzerPin = 9;
const int threshold = 500;

void setup() {
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lightLevel = analogRead(photoresistorPin);
  
  Serial.print("Light Level: ");
  Serial.println(lightLevel);

  if (lightLevel > threshold) {
    digitalWrite(buzzerPin, HIGH);
  } else {
    digitalWrite(buzzerPin, LOW);
  }

  delay(100);
}
